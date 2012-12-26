#**************************************************#
# file   : display.py                              #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Handles the window, keyboard and mouse input,    #
# drawing of objects and openGL setup              #
#**************************************************#

## Pyglet imports
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

## Lepton imports
from lepton import default_system as lepton_system
from lepton.controller import Lifetime, Movement, Fader

## Basic python imports
import math, random, importlib

## CDER imports
from core.interface import Interface
from core.minitext  import MiniText
from particle.particle import Particle
import utils
from reader.reader import CUT_NO_SELECTION

## imports to load file with appropriate reader
from config import filename, treename, filereader
reader_module = importlib.import_module('core.reader.%s' % filereader)


####################################################
class Display(pyglet.window.Window):

    ## --------------------------------------- ##
    def __init__(self, calorimeters, beam):
        """
        Constructor
        """

        ## Configure the parent class
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(Display, self).__init__(resizable=True, config=config)
        
        self.mouse_y_rotation = -57.0
        self.mouse_z_rotation = -20.0
        self.mouse_zoom = 15.0

        ## Window size
        self.width=800
        self.height=600


        self.calorimeters = calorimeters
        self.particles = []
        self.beam = beam

        ## Particle reader
        self.reader = reader_module.Custom_Reader(filename, treename)

        ## Interface
        self.interface = Interface(self.width, self.height)

        ## Controllers
        self.allow_update = False

        ## Time control
        self.refresh_rate = 30
        self.wait = 0

        ## Input text
        self.text_input_mode = False
        self.text = MiniText(70)
        
        self.setup()


    ## ---------------------------------------- ##
    def setup(self):
        """
        Setup the window size, and OpenGL drawing area
        """
        
        pyglet.clock.schedule_interval(self.update, 1.0/self.refresh_rate)

        ## Control particles from the default system
        lepton_system.add_global_controller(
            Movement(min_velocity=0.0),
            Lifetime(1.0),
            Fader(max_alpha=0.7, fade_out_start=0.05, fade_out_end=0.2),
            )


    ## ---------------------------------------- ##
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.mouse_y_rotation += dx * 0.5
            self.mouse_z_rotation += dy * 0.5

            if self.mouse_z_rotation > 85.0:
                self.mouse_z_rotation = 85.0

            if self.mouse_z_rotation < -85.0:
                self.mouse_z_rotation = -85.0

            if self.mouse_y_rotation > 180.0:
                self.mouse_y_rotation = self.mouse_y_rotation - 360.0

            if self.mouse_y_rotation < -180.0:
                self.mouse_y_rotation = self.mouse_y_rotation + 360.0


    # ---------------------------------------- ##
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):

        self.mouse_zoom += 0.1*scroll_y
        
        if self.mouse_zoom < 1.3:
            self.mouse_zoom = 1.3
        if self.mouse_zoom > 25.0:
            self.mouse_zoom = 25.0

        
    ## ---------------------------------------- ##
    def on_draw(self):
        """
        Overrides the handler to draw the pyglet window
        """
        ## When the window is drawn, draw the OpenGL content
        self.draw()


    ## ---------------------------------------- ##
    def update(self, dt):

        ## Update beam
        self.beam.update(dt)
            
        if not self.beam.incoming:
            if self.allow_update:
                all_hit = True
                for particle in self.particles:
                    particle.show()
                    if not particle.calo_hit_EM and not particle.calo_hit_HAD:
                        all_hit = False
                if not all_hit:
                    for calo in self.calorimeters:
                        calo.energize(self.particles)
                else:
                    self.allow_update = False

        ## Update particles
        for particle in self.particles:
            particle.update(dt)

        ## Update particle systems
        lepton_system.update(dt) 
                
        ## Update calorimeters
        for calo in self.calorimeters:
            calo.update(dt)

        ## Update interface
        if self.text_input_mode:
            self.text.update(dt)
            self.interface.set_text(self.text.full_output)
            
        self.interface.update(dt)
        

        self.draw()
            

    ## ---------------------------------------- ##
    def on_resize(self,width, height):
        """
        Overrides the handler to resize the pyglet window (resize OpenGL instead)
        """
        ## When the window is resized, resize the OpenGL content
        self.resize(width, height)


    ## ---------------------------------------- ##
    def resize(self, width, height):
        """
        Controls the resizing of the OpenGL display area
        """

        ## Protect against vanishing window
        if height == 0:
            height=1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        self.interface.resize(width, height)



    ## ---------------------------------------- ##
    def mode_3D(self):
        
        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.width) / float(self.height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    ## ---------------------------------------- ##
    def mode_2D(self):
        glDisable(GL_DEPTH_TEST) 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
        
        
    ## ---------------------------------------- ##
    def draw(self):
        """
        The main drawing function (determines what to draw)
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.mode_3D()
        
        ## Position camera
        gluLookAt( 0.0,  0.0, -self.mouse_zoom,
                   0.0,  0.0,  0.0,
                   0.0,  1.0,  0.0 )

        glRotatef(self.mouse_y_rotation, 0.0, 1.0, 0.0)

        phi_camera = self.mouse_y_rotation*math.pi / 180.0
        theta_camera = self.mouse_z_rotation*math.pi / 180.0
        
        glRotatef(self.mouse_z_rotation, math.cos(phi_camera), 0.0, math.sin(phi_camera))

        ## Draw lepton particles
        lepton_system.draw()

        ## Figure out the z angle in the calorimeter cylindrical coordinate system
        theta_camera += math.pi/2
        
        theta_calo, phi_calo = utils.sphy_to_sphz(theta_camera, phi_camera) 

        if phi_camera > 0:
            theta_camera = -theta_camera
        
        ## Draw calorimeters
        for calo in self.calorimeters:
            calo.theta_camera = theta_calo
            calo.r_camera = self.mouse_zoom
            calo.phi_camera = theta_camera - math.pi/2
            calo.draw()

        ## Display logo
        self.mode_2D()
        self.interface.draw()

        self.mode_3D()
        

    ## ---------------------------------------- ##
    def on_text(self, text):
        if self.text_input_mode:
            if self.negate_key:
                self.negate_key = False
            else:
                self.text.insert(text)
                self.interface.set_text(self.text.full_output)
        

    ## ---------------------------------------- ##
    def on_key_press(self, symbol, modifiers):
        """
        Make sure everything disappears correctly
        """

        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')

        if symbol == key.ENTER:
            if self.text_input_mode:
                self.text_input_mode = False
                if self.interface.cut.opacity > 0:
                    self.text.reset()
                    self.interface.set_text('')
                    self.interface.toggle_cut()
                self.reader.cut(self.text.text_output)

        if self.text_input_mode:
            if symbol == key.BACKSPACE:
                self.text.backspace()
                self.interface.set_text(self.text.full_output)

            if symbol == key.DELETE:
                self.text.delete()
                self.interface.set_text(self.text.full_output)

            if symbol == key.LEFT:
                self.text.shift_left()
                self.interface.set_text(self.text.full_output)

            if symbol == key.RIGHT:
                self.text.shift_right()
                self.interface.set_text(self.text.full_output)

            if symbol == key.UP:
                self.previous_cut +=1
                n = len(self.reader.history)
                if self.previous_cut >= n:
                    self.previous_cut = n-1
                else:
                    self.text.set(self.reader.history[self.previous_cut])
                    self.interface.set_text(self.text.full_output)

            if symbol == key.DOWN:
                self.previous_cut -=1
                if self.previous_cut < 0:
                    self.previous_cut = -1
                    self.text.set('')
                else:
                    self.text.set(self.reader.history[self.previous_cut])
                    self.interface.set_text(self.text.full_output)
                

            if symbol == key.A and modifiers & key.MOD_CTRL:
                self.text.goto_begin()

            if symbol == key.E and modifiers & key.MOD_CTRL:
                self.text.goto_end()

            if symbol == key.K and modifiers & key.MOD_CTRL:
                self.text.kill()

            if symbol == key.Y and modifiers & key.MOD_CTRL:
                self.text.yank()

        else:
            if symbol == key.C:
                self.text_input_mode = True
                self.negate_key = True
                self.input_string    = ''
                self.interface.toggle_cut()
                self.previous_cut = -1

            if symbol == key.R:
                if self.reader.current_cut != CUT_NO_SELECTION:
                    self.reader.reset_cut()
                    self.interface.reset_cut()

            if symbol == key.A:
                self.mouse_y_rotation = 0.0
                self.mouse_z_rotation = 0.0
                self.mouse_zoom = 15.0

            if symbol == key.S:
                self.mouse_y_rotation = -90.0
                self.mouse_z_rotation = 0.0
                self.mouse_zoom = 15.0

            if symbol == key.H:
                self.interface.toggle_help()

            if symbol == key.LEFT or symbol == key.RIGHT or symbol == key.UP or symbol == key.DOWN:

                ## Remove existing particles
                for particle in self.particles:
                    particle.hide()
                    lepton_system.remove_group(particle.group)
                    lepton_system.remove_group(particle.sparks)
            
                for calo in self.calorimeters:
                    calo.reset()

                self.particles = []

                if symbol == key.LEFT:
                    self.particles = self.reader.previous()

                if symbol == key.RIGHT:
                    self.particles = self.reader.next()

                if symbol == key.UP or symbol == key.DOWN:
                    self.particles = self.reader.random()

                self.reader.print_event()

                self.beam.start()
                self.allow_update = True
