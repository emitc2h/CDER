#**************************************************#
# file   : core/particle/particle.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A single particle making up the objects to be    #
# displayed. Also provides information to interact #
# with the calorimeters                            #
#**************************************************#

## Pyglet imports
from pyglet import image
from pyglet.gl import *

## Lepton imports
from lepton import Particle as lepParticle, ParticleGroup, domain, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Lifetime

## Basic python imports
import os, math, time

## CDER imports
from ..utils import *
from ..config import *

####################################################
class Particle():

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi, color, isEM=True, isHAD=True, is_min_ion=False, wide=False):
        """
        Constructor
        """

        ## Particle characteristics ##
        #----------------------------#

        ## Basic kinematics
        self.pt  = pt
        self.eta = eta
        self.phi = phi

        ## Does the particle interact with EM and/or HAD calorimeters?
        self.isEM  = isEM
        self.isHAD = isHAD

        ## Time sensitive indicators for particle travel animation and
        ## calorimeter animation
        self.r   = 0.0
        self.is_travelling = False
        self.calo_hit_EM = False
        self.calo_hit_HAD = False

        ## Does the particle pass through the calorimeters?
        self.is_min_ion = is_min_ion

        

        ## Particle domain geometry ##
        #----------------------------#
        
        ## If the particle is minimum-ionizing, make it cross the calorimeter
        if self.is_min_ion:
            self.end_r = 3*em_inner_radius
            ## Change the endcap boundary
            em_inner_z = 3*(1.0 - em_endcap_thickness/2)*eta_to_z((em_outer_radius, em_max_abs_eta))

        ## If the particle is not mimimum-ionizing, set the boundaries to the interior of the
        ## EM calorimeter
        else:
            self.end_r = em_inner_radius
            em_inner_z = (1.0 - em_endcap_thickness/2)*eta_to_z((em_outer_radius, em_max_abs_eta))

        ## Calculate the cartesian coordinate of the particle to know 
        ## if it ends up in the barrel or in the endcap
        cartesian_endpoint = rap_to_cart((em_inner_radius, self.eta, self.phi))

        ## Check that z is above em endcap
        self.in_barrel = False
            
        ## Identify if the particle ends up in the barrel region,
        ## Change the endpoint radial distance accordingly
        if abs(cartesian_endpoint[2]) >= em_inner_z:
            self.in_barrel = True
            self.end_r = (em_inner_z/abs(cartesian_endpoint[2]))*em_inner_radius

        ## Calculate the new cartesian endpoint
        cartesian_endpoint = rap_to_cart((self.r, self.eta, self.phi))

        ## Define the particle domain
        self.particle_line = domain.Line((0.0, 0.0, 0.0),
                                         cartesian_endpoint)



        ## Particle display properties ##
        #-------------------------------#

        ## Calculate rate of apparition of wisps that form the particle
        ## Uniform filling independent of the length of the particle domain
        rate = (3.0/5)*particle_filling+(2.0/5)*particle_filling*abs(self.eta)
        if self.is_min_ion:
            rate *= 4

        ## particle beam width
        width =(0.05,0.05,0.0)
        if wide:
            width =(0.5,0.5,0.0)

        ## Define particle emitter
        self.particle = StaticEmitter(
            rate=rate,
            position=self.particle_line,
            template=lepParticle(
                size=width,
                color=color
                )
            )

        ## Define the sprites populating the beam
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), '../images/wisp.png'))

        ## Particle group that controls if the particle is displayed or not
        self.particle_group = ParticleGroup(controllers=[], 
                                   renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id)))

        

    ## --------------------------------------- ##
    def show(self):
        """
        Show the particle (initiate animation)
        """
        
        if not self.particle in self.particle_group.controllers:
            
            ## Set particle domain length
            self.particle_line.end_point = rap_to_cart((self.r, self.eta, self.phi))

            ## Add particle to particle group
            self.particle_group.bind_controller(self.particle)

            ## Initiate animation parameters
            self.is_travelling = True
            self.calo_hit_EM  = False
            self.calo_hit_HAD = False


            
    ## --------------------------------------- ##
    def update(self, dt):
        """
        Animate the particle
        """

        ## Elongate particle domain as long as it hasn't reached its destination
        if self.is_travelling:
            if self.r < self.end_r:
                if self.is_min_ion:
                    self.r += 3*particle_speed*math.log(self.pt/1000.0)
                else:
                    self.r += particle_speed*math.log(self.pt/1000.0)

            ## If the particle reached its destination, stop animation
            else:
                self.is_travelling = False
                self.r = self.end_r
            self.particle_line.end_point = rap_to_cart((self.r, self.eta, self.phi))


            
    ## --------------------------------------- ##
    def hide(self):
        """
        Hide the particle
        """
        
        if self.particle in self.particle_group.controllers:
            self.particle_group.unbind_controller(self.particle)


            
    ## --------------------------------------- ##
    def dR(self, cell):
        """
        Calculates dR w.r.t. a calorimeter cell
        """
        
        return math.sqrt((self.eta - cell.eta_center)**2 + delta_phi(self.phi, cell.phi_center)**2)


    
    ## --------------------------------------- ##
    def deta(self, cell):
        """
        Calculates delta eta w.r.t. a calorimeter cell
        """
        
        return abs(self.eta - cell.eta_center)


    
    ## --------------------------------------- ##
    def dphi(self, cell):
        """
        Calculates delta phi w.r.t. a calorimeter cell
        """
        
        return delta_phi(self.phi, cell.phi_center)
