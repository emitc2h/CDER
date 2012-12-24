import pyglet

class Interface():

    def __init__(self, window_width, window_height):

        ## Logo data and parameters
        self.image_logo = pyglet.resource.image('core/images/logo_transparent.png')
        self.max_scale_logo = 0.15

        ## Help data and parameters
        self.image_help = pyglet.resource.image('core/images/help.png')
        self.image_help.anchor_x = self.image_help.width/2
        self.image_help.anchor_y = self.image_help.height/2

        self.help_opacity   = 0
        self.help_appear    = False
        self.help_disappear = False

        self.image_help_pointer = pyglet.resource.image('core/images/help_pointer.png')

        ## Show everything
        self.resize(window_width, window_height)


    def resize(self, window_width, window_height):

        scale = 1.0
        
        if window_width < 400:
            scale *= float(window_width) / 400

        if window_height < 300:
            scale *= float(window_height) / 300

        self.logo = pyglet.sprite.Sprite(self.image_logo,
                                         x=window_width - int(self.image_logo.width * scale * self.max_scale_logo * 1.1),
                                         y=int(self.image_logo.height * scale * self.max_scale_logo * 0.1))

        self.logo.scale = scale * self.max_scale_logo

        self.help = pyglet.sprite.Sprite(self.image_help,
                                         x=window_width/2,
                                         y=window_height/2)

        self.help.scale = 0.4 * scale

        self.help.opacity = self.help_opacity

        self.help_pointer = pyglet.sprite.Sprite(self.image_help_pointer,
                                         x=int(self.image_logo.width * 0.4 * scale * 0.05),
                                         y=int(self.image_logo.height * 0.4 * scale * 0.05))

        self.help_pointer.scale = 0.4 * scale
        

    def update(self, dt):

        if self.help_appear:
            self.help_opacity += 20
        if self.help_opacity > 255:
            self.help_opacity = 255
            self.help_appear = False

        if self.help_disappear:
            self.help_opacity -= 20
        if self.help_opacity < 0:
            self.help_opacity = 0
            self.help_disappear = False

        self.help.opacity = self.help_opacity
        
        
    def draw(self):
        self.logo.draw()
        if self.help_opacity > 0:
            self.help.draw()
        else:
            self.help_pointer.draw()


    def toggle_help(self):

        action = 0
        
        if self.help_opacity == 0 or self.help_disappear:
            action = 0
        if self.help_opacity == 255 or self.help_appear:
            action = 1

        if action == 0:
            self.help_appear    = True
            self.help_disappear = False
            #self.help_pointer.visible = False

        if action == 1:
            self.help_appear    = False
            self.help_disappear = True
            #self.help_pointer.visible = True

