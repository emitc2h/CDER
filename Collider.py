import pyglet

####################################################
## Instantiate objects
from core.calorimeter import em, had
objects = [em.EM_Calorimeter(),
           had.HAD_Calorimeter()]

from core.particle import particle
particles = [particle.Particle(50000, 1.2, 0.8, 1, (0.0, 0.7, 0.7)),
             particle.Particle(10000, 0.6, -2.4, 1, (0.7, 0.7, 0.0)),
             particle.Particle(160000, -0.4, 2.4, 1, (0.9, 0.1, 0.0)),
             particle.Particle(100000, -1.4, -1.2, 1, (0.1, 0.1, 0.9)),
             particle.Particle(50000, 1.3, 0.8, 1, (0.0, 0.7, 0.7)),
             particle.Particle(10000, 0.7, -2.4, 1, (0.7, 0.7, 0.0)),
             particle.Particle(160000, -0.5, 2.4, 1, (0.9, 0.1, 0.0)),
             particle.Particle(100000, -1.5, -1.2, 1, (0.1, 0.1, 0.9)),
             particle.Particle(50000, 1.4, 0.9, 1, (0.0, 0.7, 0.7)),
             particle.Particle(10000, 0.8, -2.5, 1, (0.7, 0.7, 0.0)),
             particle.Particle(160000, -0.6, 2.5, 1, (0.9, 0.1, 0.0)),
             particle.Particle(100000, -1.6, -1.3, 1, (0.1, 0.1, 0.9))]

from core.particle import beamline
beam = beamline.Beamline(particles)

####################################################
## Instantiate Display
from core.display import Display
from pyglet.gl import *

display = Display(objects, beam)
display.clear()

glEnable(GL_BLEND)
glShadeModel(GL_SMOOTH)
glBlendFunc(GL_SRC_ALPHA,GL_ONE)
glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
glDisable(GL_DEPTH_TEST)


####################################################
## Drawing handler, interface
@display.event
def on_draw():
    display.clear()
    glLoadIdentity()

        
####################################################
## Run pyglet:
if __name__ == '__main__':
    display.set_visible(True)
    pyglet.app.run()

