import pyglet

class Interface():

    def __init__(self, window_width, window_height):

        self.image_logo = pyglet.resource.image('core/logo.png')

        self.max_scale_logo = 0.15
        
        self.resize(window_width, window_height)


    def resize(self, window_width, window_height):

        scale = self.max_scale_logo
        
        if window_width < 400:
            scale *= float(window_width) / 400

        if window_height < 300:
            scale *= float(window_height) / 300

        self.logo = pyglet.sprite.Sprite(self.image_logo,
                                         x=window_width - int(self.image_logo.width * scale * 1.1),
                                         y=int(self.image_logo.height * scale * 0.1))

        self.logo.scale = scale
        
        
        
    def draw(self):
        self.logo.draw()
