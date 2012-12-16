import pyglet

####################################################
## Instantiate objects
from core.calorimeter import em, had
import math

objects = [em.EM_Calorimeter(),
           had.HAD_Calorimeter()]


####################################################
## Instantiate Display
from core.display import Display

display = Display(objects)
display.clear()


####################################################
## Drawing handler
from pyglet.gl import *

@display.event
def on_draw():
    display.clear()

        
####################################################
## Run pyglet:

if __name__ == '__main__':
    display.set_visible(True)
    pyglet.app.run()

