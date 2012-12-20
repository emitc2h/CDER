import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from lepton import default_system as lepton_system
from lepton.controller import Lifetime, Movement, Fader
import math
from particle.particle import Particle
import random
import utils

####################################################
## A class inheriting from the pyglet window      ##
## to display the openGL objects                  ##
## Author : Michel Trottier-McDonald              ##
## Date   : December 2012                         ##
####################################################
class Display(pyglet.window.Window):

    ## --------------------------------------- ##
    def __init__(self, calorimeters, beam, particles):
        """
        Constructor
        """
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(Display, self).__init__(resizable=True, config=config)

        self.mouse_y_rotation = -57.0
        self.mouse_z_rotation = -20.0
        self.mouse_zoom = 15.0

        self.calorimeters = calorimeters
        self.particles = particles
        self.beam = beam

        ## Controllers to limit redundant execution
        self.allow_update = False
        
        self.refresh_rate = 30
        self.wait = 0
        
        self.setup()


    ## ---------------------------------------- ##
    def setup(self):
        """
        Setup the window size, and OpenGL drawing area
        """
        self.width=800
        self.height=600
        
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

        ## Update particles
        if self.allow_update:
            if not self.beam.incoming:
                for particle in self.particles:
                    particle.show()
                for calo in self.calorimeters:
                    calo.energize(self.particles)
                self.allow_update = False

        ## Update particle systems
        lepton_system.update(dt) 
                
        ## Update calorimeters
        for calo in self.calorimeters:
            calo.update(dt)

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
        
        
    ## ---------------------------------------- ##
    def draw(self):
        """
        The main drawing function (determines what to draw)
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

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


    ## ---------------------------------------- ##
    def on_key_press(self, symbol, modifiers):
        """
        Make sure everything disappears correctly
        """
        
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')

        if symbol == key.LEFT or symbol == key.RIGHT:

            ## Remove existing particles
            for particle in self.particles:
                particle.hide()
                lepton_system.remove_group(particle.group)
                lepton_system.remove_group(particle.sparks)
            for calo in self.calorimeters:
                calo.reset()

            self.particles = []
            
            ## Generate a random set of particles
            n = random.randint(10,50)
            for i in range(n):
                color_random1 = random.random()
                color_random2 = random.random()
                color_random3 = random.random()
                R = 0.5 - 0.5*color_random1 + 0.5*color_random2
                G = 0.5 - 0.5*color_random2 + 0.5*color_random3
                B = 0.5 - 0.5*color_random3 + 0.5*color_random1
                new_particle = Particle(pt=random.random()*100000,
                                        eta=(random.random()-0.5)*4.0,
                                        phi=random.random()*2*math.pi,
                                        n=1,
                                        color=(R,G,B),
                                        isEM=True,
                                        isHAD=random.randint(0,1))
                self.particles.append(new_particle)
            
            self.beam.start()
            self.allow_update = True
