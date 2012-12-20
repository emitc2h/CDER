import os
import math
import time
from pyglet import image
from pyglet.gl import *

from ..utils import *
from ..config import *

from lepton import Particle as lepParticle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Lifetime
from lepton import domain

class Particle():

    def __init__(self, pt, eta, phi, color, isEM = True, isHAD = True):

        self.r   = 0.0
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
        cartesian_endpoint = rap_to_cart((em_inner_radius, self.eta, self.phi))

        ## Check that z is above em endcap
        self.in_barrel = False
        self.is_travelling = False
        self.calo_hit_EM = False
        self.calo_hit_HAD = False
        self.end_r = em_inner_radius
        em_inner_z = (1.0 - em_endcap_thickness/2)*eta_to_z((em_outer_radius, em_max_abs_eta))
        if abs(cartesian_endpoint[2]) >= em_inner_z:
            self.in_barrel = True
            self.end_r = (em_inner_z/abs(cartesian_endpoint[2]))*em_inner_radius

        cartesian_endpoint = rap_to_cart((self.r, self.eta, self.phi))
        
        self.particle_line = domain.Line((0.0, 0.0, 0.0),
                                         cartesian_endpoint)

        ## A beam emitter
        self.particle = StaticEmitter(
            rate= (3.0/5)*particle_filling+(2.0/5)*particle_filling*abs(self.eta),
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
            self.particle_line.end_point = rap_to_cart((self.r, self.eta, self.phi))
            self.group.bind_controller(self.particle)
            self.is_travelling = True
            self.calo_hit_EM  = False
            self.calo_hit_HAD = False

    def update(self, dt):
        if self.is_travelling:
            if self.r < self.end_r:
                self.r += particle_speed*math.log(self.pt/1000.0)
            else:
                self.is_travelling = False
                self.r = self.end_r
            self.particle_line.end_point = rap_to_cart((self.r, self.eta, self.phi))
        
    
    def hide(self):
        if self.particle in self.group.controllers:
            self.group.unbind_controller(self.particle)

    def dR(self, cell):
        return math.sqrt((self.eta - cell.eta_center)**2 + delta_phi(self.phi, cell.phi_center)**2)

    def deta(self, cell):
        return abs(self.eta - cell.eta_center)

    def dphi(self, cell):
        return delta_phi(self.phi, cell.phi_center)
