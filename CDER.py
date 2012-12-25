import pyglet
from core import config

####################################################
## Instantiate objects
from core.calorimeter import em, had
calorimeters = []
if config.display_em  : calorimeters.append(em.EM_Calorimeter())
if config.display_had : calorimeters.append(had.HAD_Calorimeter())
    
particles = []

from core.particle import beamline
beam = beamline.Beamline()


####################################################
## Instantiate Display
from core.display import Display
from pyglet.gl import *

display = Display(calorimeters, beam, particles)
display.clear()


####################################################
## Drawing handler, interface
@display.event
def on_draw():
    display.clear()
    glLoadIdentity()

        
####################################################
## Run pyglet:
if __name__ == '__main__':
    pyglet.app.run()

