import pyglet

####################################################
## Instantiate objects
from core.calorimeter import cell, ring
import math

cells = [
    ring.Ring((0.20, 0.65, -0.9, 0.2), 10, cell.GEO_CYLINDRICAL),
    ring.Ring((0.7, 0.8, -0.9, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, -0.6, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, -0.3, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, 0.0, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, 0.3, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, 0.6, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.7, 0.8, 0.9, 0.2), 20, cell.GEO_PROJECTIVE),
    ring.Ring((0.20, 0.65, 0.9, 0.2), 10, cell.GEO_CYLINDRICAL)
    ]


####################################################
## Instantiate Display
from core.display import Display

display = Display(cells)
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

