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
from lepton.controller import Lifetime
from lepton import domain

class Particle():

    def __init__(self, pt, eta, phi, n, color, isEM = True, isHAD = True):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.isEM  = isEM
        self.isHAD = isHAD
        
        ## Define the sprites populating the beam
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'wisp.png'))
        self.sparks = ParticleGroup(
            controllers=[Lifetime(0.2)],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id)))

        spark = [self.spark_tex]
        
        ## Particle line domain
        self.particle_line = domain.Line((0.0, 0.0, 0.0),
                                         rap_to_cart((1.5, self.eta, self.phi)))

        ## A beam emitter
        self.particle = StaticEmitter(
            rate= 750+500*abs(self.eta),
            position=self.particle_line,
            template=lepParticle(
                size=(0.05,0.05,0.0),
                color=color
                )
            )
        
        self.group = ParticleGroup(controllers=[], 
                                   renderer=BillboardRenderer(SpriteTexturizer.from_images(spark)))
        
    def show(self):
        if not self.particle in self.group.controllers:
            self.group.bind_controller(self.particle)
    
    def hide(self):
        if self.particle in self.group.controllers:
            self.group.unbind_controller(self.particle)

    def dR(self, cell):
        return math.sqrt((self.eta - cell.eta_center)**2 + delta_phi(self.phi, cell.phi_center)**2)

    def deta(self, cell):
        return abs(self.eta - cell.eta_center)

    def dphi(self, cell):
        return delta_phi(self.phi, cell.phi_center)
