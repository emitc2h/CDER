import pyglet

####################################################
## Instantiate objects
from core.calorimeter import em, had
objects = [em.EM_Calorimeter(),
           had.HAD_Calorimeter()]

from core.particle import beamline
particles = [beamline.Beamline()]


####################################################
## Instantiate Display
from core.display import Display
from pyglet.gl import *

display = Display(objects, particles)
display.clear()

glEnable(GL_BLEND)
glShadeModel(GL_SMOOTH)
glBlendFunc(GL_SRC_ALPHA,GL_ONE)
glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
glDisable(GL_DEPTH_TEST)


####################################################
## Drawing handler

@display.event
def on_draw():
    display.clear()
    glLoadIdentity()


        
####################################################
## Run pyglet:
if __name__ == '__main__':
    display.set_visible(True)
    pyglet.app.run()

