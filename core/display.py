#**************************************************#
# file   : core/display.py                         #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Handles the window, keyboard and mouse input,    #
# drawing of objects and openGL setup              #
#**************************************************#

#############################################################################
#   Copyright 2012-2013 Michel Trottier-McDonald                            #
#                                                                           #
#   This file is part of CDER.                                              #
#                                                                           #
#   CDER is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   CDER is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
#############################################################################

## Pyglet imports
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

## Basic python imports
import math, random, importlib

## CDER imports
from core.interface import Interface
from core.minitext  import MiniText
from particle.particle import Particle
import utils, config
from reader.reader import CUT_NO_SELECTION

## imports to load file with appropriate reader
reader_module = importlib.import_module('core.reader.%s' % config.filereader)


####################################################
class Display(pyglet.window.Window):

    ## --------------------------------------- ##
    def __init__(self, calorimeters, beam):
        """
        Constructor
        """

        ## Configure the parent class
        window_config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(Display, self).__init__(resizable=True,
                                      config=window_config)

        ## Initial point of view
        self.yaw = -90.0
        self.pitch = -20.0
        self.zoom = 15.0

        ## Automatic rotation
        self.omega = config.camera_rotation_speed
        self.rotating = True

        ## Window size
        self.width=800
        self.height=600

        ## 3D objects
        self.calorimeters = calorimeters
        self.particles = []
        self.beam = beam

        ## 2D objects
        self.interface = Interface(self.width, self.height)
        
        ## input ROOT file management
        self.reader = reader_module.Custom_Reader(config.filename,
                                                  config.treename)

        ## Control when to allow modification of calorimeter openGL primitives
        self.allow_calo_update = False

        ## Time control
        self.refresh_rate = 30

        ## Mini text editor for cuts
        self.text_input_mode = False
        self.text_editor = MiniText(70)

        ## pyglet time control
        pyglet.clock.schedule_interval(self.update, 1.0/self.refresh_rate)

    


    ## ---------------------------------------- ##
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        Mouse control 1: click and drag to rotate around the scene
        """

        ## Click
        if buttons == mouse.LEFT:

            ## translate mouse movement into rotation of point of view
            self.yaw += dx * config.yaw_speed
            self.pitch += dy * config.pitch_speed

            ## Do not allow periodicity on pitch
            if self.pitch > config.max_pitch:
                self.pitch = config.max_pitch

            if self.pitch < config.min_pitch:
                self.pitch = config.min_pitch

            ## Do not allow yaw to grow arbitrarily large
            if self.yaw > 180.0:
                self.yaw = self.yaw - 360.0

            if self.yaw < -180.0:
                self.yaw = self.yaw + 360.0

                

    # ---------------------------------------- ##
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        Mouse control 2: scroll up and down to zoom in and out
        """

        ## Translate mouse scroll into zoom
        self.zoom += scroll_y * config.zoom_speed

        ## Only allow zoom in specified range
        if self.zoom < config.max_zoom:
            self.zoom = config.max_zoom
        if self.zoom > config.min_zoom:
            self.zoom = config.min_zoom



    ## ---------------------------------------- ##
    def on_text(self, text):
        """
        Keyboard control 1: typing in the text editor
        """

        ## Must be in text input mode, otherwise keys for control
        if self.text_input_mode:
            ## Prevent 'c' (used to trigger text input mode) to be included in text editor
            if self.negate_key:
                self.negate_key = False
            else:
                ## Collect character into text editor and pass formatted output to
                ## 2D inteface
                self.text_editor.insert(text)
                self.interface.set_text(self.text_editor.full_output)



    ## ---------------------------------------- ##
    def on_key_press(self, symbol, modifiers):
        """
        Keyboard control 2: main controls
        """

        ## Main controls
        if not self.text_input_mode:

            ## Turn on text input mode, enter cut
            if symbol == key.C:
                self.text_input_mode = True
                self.negate_key = True
                ## Display cut message
                self.interface.toggle_cut()
                ## Cut history navigator
                self.history_index = -1

            ## Reset the cut, go back to full ROOT tree 
            if symbol == key.R:
                if self.reader.current_cut != CUT_NO_SELECTION:
                    self.reader.reset_cut()
                    self.interface.reset_cut()

            ## Transverse view
            if symbol == key.A:
                ## Stop automatic rotation
                self.rotating = False
                
                self.yaw = 0.0
                self.pitch = 0.0
                self.zoom = 15.0

            ## Longitudinal view
            if symbol == key.S:
                ## Stop automatic rotation
                self.rotating = False
                
                self.yaw = -90.0
                self.pitch = 0.0
                self.zoom = 15.0

            ## Toggle automatic rotation
            if symbol == key.D:
                if not self.rotating:
                    self.rotating = True
                elif self.rotating:
                    self.rotating = False

            ## Toggle help screen
            if symbol == key.H:
                self.interface.toggle_help()

            ## Event navigation
            if symbol == key.LEFT or symbol == key.RIGHT or symbol == key.UP or symbol == key.DOWN:

                ## Load particles from previous event
                if symbol == key.LEFT:
                    new_particles = self.reader.previous()

                ## Load particles from next event
                if symbol == key.RIGHT:
                    new_particles = self.reader.next()

                ## Load particles from a random event
                if symbol == key.UP or symbol == key.DOWN:
                    new_particles = self.reader.random()

                if new_particles is not None:
                    
                    ## Prepare for new event, remove particles from old event
                    for particle in self.particles:
                        particle.delete()

                    self.particles = new_particles

                    ## Remove calorimeter energy
                    for calo in self.calorimeters:
                        calo.reset()
                        calo.energize(self.particles)

                    ## Print out event information to terminal
                    self.reader.print_event()

                    ## Beam collision animation
                    self.beam.start()

                    ## Allow modification of calorimeter openGL primitives
                    self.allow_calo_update = True


        ## Text editor controls
        if self.text_input_mode:

            ## Backspace expected behaviour
            if symbol == key.BACKSPACE:
                self.text_editor.backspace()
                self.interface.set_text(self.text_editor.full_output)

            ## Delete expected behaviour
            if symbol == key.DELETE:
                self.text_editor.delete()
                self.interface.set_text(self.text_editor.full_output)

            ## Move cursor left
            if symbol == key.LEFT:
                self.text_editor.cursor_left()
                self.interface.set_text(self.text_editor.full_output)

            ## Move cursor right
            if symbol == key.RIGHT:
                self.text_editor.cursor_right()
                self.interface.set_text(self.text_editor.full_output)

            ## Move back one step in history
            if symbol == key.UP:
                if self.history_index == -1:
                    self.current_input = self.text_editor.text_output
                self.history_index +=1
                n = len(self.reader.history)
                if self.history_index >= n:
                    self.history_index = n-1
                else:
                    self.text_editor.set(self.reader.history[self.history_index])
                    self.interface.set_text(self.text_editor.full_output)

            ## Move forward one step in history
            if symbol == key.DOWN:
                self.history_index -=1
                
                if self.history_index < 0:
                    self.history_index = -1
                    self.text_editor.set(self.current_input)
                else:
                    self.text_editor.set(self.reader.history[self.history_index])
                    self.interface.set_text(self.text_editor.full_output)
                

            ## Move cursor to beginning of text
            if symbol == key.A and modifiers & key.MOD_CTRL:
                self.text_editor.goto_begin()

            ## Move cursor to end of text
            if symbol == key.E and modifiers & key.MOD_CTRL:
                self.text_editor.goto_end()

            ## Kill the text following te cursor
            if symbol == key.K and modifiers & key.MOD_CTRL:
                self.text_editor.kill()

            ## Yank the text back at the cursor position
            if symbol == key.Y and modifiers & key.MOD_CTRL:
                self.text_editor.yank()

        ## Terminate text input mode and pass cut string to ROOT file reader
        if symbol == key.ENTER:
            ## Terminate text input mode
            if self.text_input_mode:
                self.text_input_mode = False
                ## Empty text editor and interface text, make cut message disappear
                if self.interface.cut.opacity > 0:
                    self.text_editor.reset()
                    self.interface.set_text('')
                    self.interface.toggle_cut()
                ## Pass cut string to ROOT file reader
                if self.reader.cut(self.text_editor.text_output):

                    ## Prepare for new event, remove particles from old event
                    for particle in self.particles:
                        particle.delete()
# 
                    self.particles = []
                    
                    ## Remove calorimeter energy
                    for calo in self.calorimeters:
                        calo.reset()
                        calo.energize(self.particles)
                        
                
                    ## Select a random event that passes the cut, print and display
                    self.particles = self.reader.random()
                    self.reader.print_event()
                    self.beam.start()
                    self.allow_calo_update = True
                

        ## Quit CDER
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')



    ## ---------------------------------------- ##
    def on_resize(self,width, height):
        """
        Behaviour of displayed objects when resizing the window
        """

        ## Avoid displaying artefacts in memory
        self.clear()
        
        ## Protect against vanishing window
        if height == 0:
            height=1

        ## Adjust openGL 3D perspective
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        ## Adjust positioning and size of 2D objects
        self.interface.resize(width, height)



    ## ---------------------------------------- ##
    def mode_3D(self):
        """
        Set openGL to draw objects in the 3D scene
        """

        ## Rendering options
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);

        ## Perspective definition
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.width) / float(self.height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



    ## ---------------------------------------- ##
    def mode_2D(self):
        """
        Set openGL to draw objects in the 2D scene in front of the 3D scene
        """

        ## Rendering options
        #glDisable(GL_DEPTH_TEST) 

        ## Perspective options
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        


    ## ---------------------------------------- ##
    def update(self, dt):
        """
        Update the displayed 3D and 2D scenes
        """

        ## Automatic rotation
        if self.rotating:
            self.yaw += self.omega * dt
            ## Do not allow yaw to grow arbitrarily large
            if self.yaw > 180.0:
                self.yaw = self.yaw - 360.0
            if self.yaw < -180.0:
                self.yaw = self.yaw + 360.0
        
        ## Update beam positions (only during beam animation)
        if self.beam.incoming:
            self.beam.update(dt)

        ## Update calorimeters
        for calo in self.calorimeters:
            calo.update(dt)

        ## Update interface
        if self.text_input_mode:
            self.text_editor.update(dt)
            self.interface.set_text(self.text_editor.full_output)
        self.interface.update(dt)

        ## Redraw the scene
        self.draw()
    
        
        
    ## ---------------------------------------- ##
    def draw(self):
        """
        Draw the 3D and 2D scenes
        """

        ## Clear openGL buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        ## Draw the 3D scene first
        self.mode_3D()
        
        ## Point of view
        gluLookAt( 0.0,  0.0, -self.zoom,
                   0.0,  0.0,  0.0,
                   0.0,  1.0,  0.0 )

        ## Rotate the scene to emulate yaw
        glRotatef(self.yaw, 0.0, 1.0, 0.0)

        ## Determine the pitch axis
        phi_camera = self.yaw*math.pi / 180.0
        theta_camera = self.pitch*math.pi / 180.0

        ## Rotate the scene to emulate pitch
        glRotatef(self.pitch, math.cos(phi_camera), 0.0, math.sin(phi_camera))

        ## Determine camera position w.r.t. calorimeter coordinate system
        ## This allow ordering of cell drawing in case of disabled depth test
        theta_camera += math.pi/2
        theta_calo, phi_calo = utils.sphy_to_sphz(theta_camera, phi_camera) 
        if phi_camera > 0:
            theta_camera = -theta_camera

        ## Draw calorimeters
        for calo in self.calorimeters:
            calo.theta_camera = theta_calo
            calo.r_camera = self.zoom
            calo.phi_camera = theta_camera - math.pi/2
            calo.draw()

        ## Draw particles
        for particle in self.particles:
            particle.draw()

        ## Draw the 2D scene, delegate to interface
        self.mode_2D()
        self.interface.draw()

        ## Switch back to 3D scene to allow for manipulation
        self.mode_3D()
