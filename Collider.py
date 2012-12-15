import pyglet

####################################################
## Instantiate objects
from core.calorimeter import em_barrel, em_endcaps, had_barrel, had_endcaps
import math

objects = [em_barrel.EM_Barrel(),
           em_endcaps.EM_Endcaps(),
           had_barrel.HAD_Barrel(),
           had_endcaps.HAD_Endcaps()]


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

