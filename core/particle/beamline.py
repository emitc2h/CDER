#**************************************************#
# file   : core/particle/beamline.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Makes a collision animation when switching to a  #
# different event                                  #
#**************************************************#

## Pyglet imports
from pyglet import image
from pyglet.gl import *

## Lepton imports
from lepton import Particle, ParticleGroup, domain, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Lifetime, Movement, Fader

## Basic python imports
import os, math, time

## CDER imports
from ..config import *

####################################################
class Beamline():

    ## --------------------------------------- ##
    def __init__(self):
        """
        Constructor
        """

        ## Sprites ##
        #-----------#
        
        ## Define the sprites used in beams and collision
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), '../images/wisp.png'))


        
        ## Beams ##
        #---------#
        
        ## Beam parameters
        self.incoming = False
        self.beam_length = beam_speed
        self.beam_start  = beam_speed*12.0 + self.beam_length/2.0
        self.beam_speed  = beam_speed
        
        ## A beam domain
        self.A_beam_position = -self.beam_start
        self.A_beam_section = domain.Line((0.0, 0.0, self.A_beam_position - self.beam_length/2),
                                          (0.0, 0.0, self.A_beam_position + self.beam_length/2))

        ## A beam emitter
        self.A_beam = StaticEmitter(
            rate=20000,
            position=self.A_beam_section,
            template=Particle(
                size=(0.1,0.1,0.0),
                color=(0.8,0.2,0.1)
                )
            )

        ## C beam domain
        self.C_beam_position = self.beam_start
        self.C_beam_section = domain.Line((0.0, 0.0, self.C_beam_position + self.beam_length/2),
                                          (0.0, 0.0, self.C_beam_position - self.beam_length/2))

        ## C beam emitter
        self.C_beam = StaticEmitter(
            rate=20000,
            position=self.C_beam_section,
            template=Particle(
                size=(0.1,0.1,0.0),
                color=(0.8,0.2,0.1)
                )
            )

        ## Particle group to hold the beams
        self.beam_group = ParticleGroup(controllers=[], 
                                   renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id))
            )


        
        ## Collision ##
        #-------------#
        
        ## Charged particles coming out of the collision
        self.collision_charged = StaticEmitter(
            template=Particle(
                position=(0, 0, 0), 
                color=(0.65, 0.25, 0.0), 
                size=(0.05, 0.05, 0)),
            deviation=Particle(
                velocity=(2.0, 2.0, 2.0),
                age=0.5)
            )

        ## Neutral particles coming out of the collision
        self.collision_neutral = StaticEmitter(
            template=Particle(
                position=(0, 0, 0), 
                color=(0.40, 0.45, 0.50), 
                size=(0.05, 0.05, 0)),
            deviation=Particle(
                velocity=(2.0, 2.0, 2.0),
                age=0.5)
            )

        ## Particle group to hold the collisions
        self.colsparks = ParticleGroup(
            controllers=[
                Lifetime(0.5),
                Movement(damping=0.83),
                Fader(fade_out_start=0.2, fade_out_end=0.5),
                ],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id))
            )


    
    ## --------------------------------------- ##
    def update(self, dt):
        """
        Behaviour of the beams in time
        """

        ## Check that beams haven't reached collision point
        ## Both beams should be perfectly sychronized, check beam A only
        if self.A_beam_position <= -self.beam_length/2:

            ## Move A beam
            self.A_beam_section.start_point = (0.0, 0.0, self.A_beam_position - self.beam_length/2)
            self.A_beam_section.end_point = (0.0, 0.0, self.A_beam_position + self.beam_length/2)
            
            ## Update A beam position
            self.A_beam_position += self.beam_speed

            ## Move C beam
            self.C_beam_section.start_point = (0.0, 0.0, self.C_beam_position + self.beam_length/2)
            self.C_beam_section.end_point = (0.0, 0.0, self.C_beam_position - self.beam_length/2)
            
            ## Update C beam position
            self.C_beam_position -= self.beam_speed

        ## When beams reach the collision point, make the collision animation
        else:
            if self.incoming:
                self.collide(0)          

            ## Make the beams disappear, the beams are not in motion anymore
            self.stop()


    
    ## --------------------------------------- ##
    def start(self):
        """
        Start the collision animation
        """

        ## Add A beam into the beam particle group and set its initial position
        if not self.A_beam in self.beam_group.controllers:
            self.A_beam_position = -self.beam_start
            self.A_beam_section.start_point = (0.0, 0.0, self.A_beam_position - self.beam_length/2)
            self.A_beam_section.end_point = (0.0, 0.0, self.A_beam_position + self.beam_length/2)
            self.beam_group.bind_controller(self.A_beam)

        ## Add C beam into the beam particle group and set its initial position
        if not self.C_beam in self.beam_group.controllers:
            self.C_beam_position = self.beam_start
            self.C_beam_section.start_point = (0.0, 0.0, self.C_beam_position - self.beam_length/2)
            self.C_beam_section.end_point = (0.0, 0.0, self.C_beam_position + self.beam_length/2)
            self.beam_group.bind_controller(self.C_beam)

        ## The beam is in motion
        self.incoming = True

        

    ## --------------------------------------- ##
    def A_stop(self):
        """
        Stop A beam
        """

        ## Remove A beam from particle group, so that it isn't displayed anymore
        if self.A_beam in self.beam_group.controllers:
            self.beam_group.unbind_controller(self.A_beam)


            
    ## --------------------------------------- ##
    def C_stop(self):
        """
        Stop C beam
        """

        ## Remove C beam from particle group so that it isn't displayed anymore
        if self.C_beam in self.beam_group.controllers:
            self.beam_group.unbind_controller(self.C_beam)


            
    ## --------------------------------------- ##
    def stop(self):
        """
        Stop both A and C beam, beams not in motion
        """
        
        if self.incoming:
            self.A_stop()
            self.C_stop()
            self.incoming = False


            
    ## --------------------------------------- ##
    def collide(self,dt):
        """
        Make the collision animation
        """
        
        self.collision_charged.emit(1200, self.colsparks)
        self.collision_neutral.emit(800, self.colsparks)
