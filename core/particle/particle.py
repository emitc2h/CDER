import os
import math
import time
from pyglet import image
from pyglet.gl import *

from ..utils import *

from lepton import Particle as lepParticle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Lifetime, Movement, Fader
from lepton import domain

class Particle():

    def __init__(self, pt, eta, phi, n, color):

        ## Define the sprites populating the beam
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'flare3.png'))
        self.sparks = ParticleGroup(
            controllers=[Lifetime(0.2)],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id)))

        spark = [self.spark_tex]
        
        ## Particle line domain
        self.particle_line = domain.Line((0.0, 0.0, 0.0),
                                         rap_to_cart((math.log(pt/10000.0 + 1), eta, phi)))

        ## A beam emitter
        self.particle = StaticEmitter(
            rate=(math.log(pt/10000.0 + 1))*1000,
            position=self.particle_line,
            template=lepParticle(
                size=(0.1,0.1,0.0),
                color=color
                )
            )


        ## Control particles from the default system
        default_system.add_global_controller(
            Movement(min_velocity=0.0),
            Lifetime(1.0),
            Fader(max_alpha=0.7, fade_out_start=0.05, fade_out_end=0.2),
            )
        
        self.group = ParticleGroup(controllers=[], 
                                   renderer=BillboardRenderer(SpriteTexturizer.from_images(spark)))

        
    def update(self, dt):
        pass
        
    def start(self):
        if not self.particle in self.group.controllers:
            self.group.bind_controller(self.particle)
    
    def stop(self):
        if self.particle in self.group.controllers:
            self.group.unbind_controller(self.particle)
