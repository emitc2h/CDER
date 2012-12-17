import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import lepton
import math
import utils

####################################################
## A class inheriting from the pyglet window      ##
## to display the openGL objects                  ##
## Author : Michel Trottier-McDonald              ##
## Date   : December 2012                         ##
####################################################
class Display(pyglet.window.Window):

    ## --------------------------------------- ##
    def __init__(self, calorimeters, particles):
        """
        Constructor
        """
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(Display, self).__init__(resizable=True, config=config)

        self.mouse_y_rotation = -57.0
        self.mouse_z_rotation = -20.0
        self.mouse_zoom = 4.0

        self.calorimeters = calorimeters
        self.particles = particles

        self.refresh_rate = 1/30.0
        
        self.setup()


    ## ---------------------------------------- ##
    def setup(self):
        """
        Setup the window size, and OpenGL drawing area
        """
        self.width=640
        self.height=480
        self.init()
        pyglet.clock.schedule_interval(self.update, self.refresh_rate)
        pyglet.clock.schedule_interval(lepton.default_system.update, self.refresh_rate)


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
        
        if self.mouse_zoom < 2.0:
            self.mouse_zoom = 2.0
        if self.mouse_zoom > 6.0:
            self.mouse_zoom = 6.0

        
    ## ---------------------------------------- ##
    def on_draw(self):
        """
        Overrides the handler to draw the pyglet window
        """
        ## When the window is drawn, draw the OpenGL content
        self.draw()


    ## ---------------------------------------- ##
    def update(self, dt):
        
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
    def init(self):
        """
        Initialize the OpenGL rendering
        """

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        
        glShadeModel(GL_SMOOTH)
        
        glMatrixMode(GL_PROJECTION)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)#_MINUS_SRC_ALPHA)

        glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);

        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)


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
        lepton.default_system.draw()

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

        if symbol == key.X:
            self.particles[0].explode()
