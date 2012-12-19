import pyglet

class Interface():

    def __init__(self):

        self.title = pyglet.text.Label(text="Collider 1.0", x=10, y=575)

    def draw(self):
        self.title.draw()
