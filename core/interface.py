import pyglet

class Interface():

    def __init__(self, window_width, window_height):

        ## Logo data and parameters
        self.image_logo = pyglet.resource.image('core/images/logo_transparent.png')
        self.max_scale_logo = 0.15

        self.logo = pyglet.sprite.Sprite(self.image_logo,
                                         x=window_width - int(self.image_logo.width * self.max_scale_logo * 1.1),
                                         y=int(self.image_logo.height * self.max_scale_logo * 0.1))

        
        ## Help data and parameters
        self.image_help = pyglet.resource.image('core/images/help.png')
        self.image_help.anchor_x = self.image_help.width/2
        self.image_help.anchor_y = self.image_help.height/2

        self.help_appear    = False
        self.help_disappear = False

        self.help = pyglet.sprite.Sprite(self.image_help,
                                         x=window_width/2,
                                         y=window_height/2)

        self.image_help_pointer = pyglet.resource.image('core/images/help_pointer.png')

        self.help_pointer = pyglet.sprite.Sprite(self.image_help_pointer,
                                                 x=int(self.image_help_pointer.width * 0.04),
                                                 y=int(self.image_help_pointer.height * 0.4))

        
        ## Cut data and parameters
        self.image_cut = pyglet.resource.image('core/images/cut_message.png')
        self.image_cut.anchor_x = self.image_cut.width/2
        self.image_cut.anchor_y = self.image_cut.height/2

        self.cut_disappear = False
        self.cut_appear = False

        self.cut = pyglet.sprite.Sprite(self.image_cut,
                                         x=window_width/2,
                                         y=window_height*0.16)

        ## Text field
        self.text_field = pyglet.text.Label('',
                                            font_name='Monaco',
                                            font_size=10,
                                            x=window_width*0.02,
                                            y=window_height*0.1,
                                            color=(73, 145, 255, 255),
                                            align='center')
        
        ## Show everything
        self.resize(window_width, window_height)

        
        ## Hide help and cut message at the beginning
        self.help.opacity = 0
        self.cut.opacity = 0


    def resize(self, window_width, window_height):

        ## Calculate scale from window size
        scale = 1.0
        if window_width < 400:
            scale *= float(window_width) / 400
        if window_height < 300:
            scale *= float(window_height) / 300

            
        ## Logo
        self.logo.x = window_width - int(self.image_logo.width * scale * self.max_scale_logo * 1.1)
        self.logo.y = int(self.image_logo.height * scale * self.max_scale_logo * 0.1)
        self.logo.scale = scale * self.max_scale_logo


        ## Help message
        self.help.scale = 0.4 * scale


        ## Help pointer
        self.help_pointer.x = int(self.image_help_pointer.width * 0.04 * scale)
        self.help_pointer.y = int(self.image_help_pointer.height * 0.4 * scale)
        self.help_pointer.scale = 0.4 * scale


        ## Cut message
        self.cut.y = window_height*0.16
        self.cut.scale = 0.4 * scale

        ## Reposition text field
        self.text_field.x = window_width*0.02
        self.text_field.y = window_height*0.1



    def set_text(self, text):
        self.text_field.text = text

    def update(self, dt):

        if self.help_appear:
            self.help.opacity += 20
        if self.help.opacity > 255:
            self.help.opacity = 255
            self.help_appear = False

        if self.help_disappear:
            self.help.opacity -= 20
        if self.help.opacity < 0:
            self.help.opacity = 0
            self.help_disappear = False

        if self.cut_appear:
            self.cut.opacity += 20
        if self.cut.opacity > 255:
            self.cut.opacity = 255
            self.cut_appear = False
        
        if self.cut_disappear:
            self.cut.opacity -= 20
        if self.cut.opacity < 0:
            self.cut.opacity = 0
            self.cut_disappear = False
        
        
    def draw(self):
        self.logo.draw()
        if self.help.opacity > 0:
            self.help.draw()
        else:
            self.help_pointer.draw()

        if self.cut.opacity > 0:
            self.cut.draw()

        self.text_field.draw()


    def toggle_help(self):

        action = 0
        
        if self.help.opacity == 0 or self.help_disappear:
            action = 0
        if self.help.opacity == 255 or self.help_appear:
            action = 1

        if action == 0:
            self.help_appear    = True
            self.help_disappear = False

        if action == 1:
            self.help_appear    = False
            self.help_disappear = True

            
    def toggle_cut(self):

        action = 0

        if self.cut.opacity == 0 or self.cut_disappear:
            action = 0
        if self.cut.opacity == 255 or self.cut_appear:
            action = 1

        if action == 0:
            self.cut_appear    = True
            self.cut_disappear = False

        if action == 1:
            self.cut_appear    = False
            self.cut_disappear = True
        

