import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import math

####################################################
## A class inheriting from the pyglet window      ##
## to display the openGL objects                  ##
## Author : Michel Trottier-McDonald              ##
## Date   : December 2012                         ##
####################################################
class Display(pyglet.window.Window):

    ## --------------------------------------- ##
    def __init__(self, objects):
        """
        Constructor
        """
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(Display, self).__init__(resizable=True, config=config)

        self.mouse_y_rotation = 0.0
        self.mouse_z_rotation = 0.0
        self.mouse_zoom = 3.0

        self.objects = objects
        
        self.setup()


    ## ---------------------------------------- ##
    def setup(self):
        """
        Setup the window size, and OpenGL drawing area
        """
        self.width=800
        self.height=600
        self.init(self.width, self.height)
        pyglet.clock.schedule_interval(self.update, 1/30.0)


    ## ---------------------------------------- ##
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.mouse_y_rotation += dx * 0.5
            self.mouse_z_rotation += dy * 0.5

            if self.mouse_z_rotation > 85.0:
                self.mouse_z_rotation = 85.0

            if self.mouse_z_rotation < -85.0:
                self.mouse_z_rotation = -85.0


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
        self.draw()


    ## ---------------------------------------- ##
    def on_resize(self,width, height):
        """
        Overrides the handler to resize the pyglet window (resize OpenGL instead)
        """
        ## When the window is resized, resize the OpenGL content
        self.resize(width, height)


    ## ---------------------------------------- ##
    def init(self, width, height):
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
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

        gluLookAt( 0.0,  0.0, -self.mouse_zoom,
                   0.0,  0.0,  0.0,
                   0.0,  1.0,  0.0 )

        glRotatef(self.mouse_y_rotation, 0.0, 1.0, 0.0)
        glRotatef(self.mouse_z_rotation, 0.0, 0.0, 1.0)

        ## Draw objects
        for obj in self.objects:
            obj.draw()


    ## ---------------------------------------- ##
    def on_key_press(self, symbol, modifiers):
        """
        Make sure everything disappears correctly
        """
        
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')
