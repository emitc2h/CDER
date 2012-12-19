import os
import math
import time
from pyglet import image
from pyglet.gl import *

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Lifetime, Movement, Fader
from lepton import domain

class Beamline():

    def __init__(self, particles):

        ## Load particles
        self.particles = particles
        
        ## Define the sprites populating the beam
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'flare3.png'))
        self.sparks = ParticleGroup(
            controllers=[Lifetime(0.2)],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id)))

        spark = [self.spark_tex]

        ## Beam parameters
        self.incoming = False
        self.beam_length = 8.0
        self.beam_start  = 100.0 + self.beam_length
        self.beam_speed  = 8.0
        
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
                color=(0.8,0.1,0.1)
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
                color=(0.1,0.8,0.1)
                )
            )

        ## Collision
        self.colsparks = ParticleGroup(
            controllers=[
                Lifetime(1.0),
                Movement(damping=0.93),
                Fader(fade_out_start=0.4, fade_out_end=1.0),
                ],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.get_texture().id))
            )
        
        self.collision = StaticEmitter(
            template=Particle(
                position=(0, 0, 0), 
                color=(1.0 ,0.7, 0.0), 
                size=(0.1, 0.1, 0)),
            deviation=Particle(
                position=(0.05, 0.05, 0.05), 
                velocity=(0.8, 0.8, 0.8),
                age=1.5)
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

        if self.A_beam_position <= -self.beam_length/2:
            self.A_beam_section.start_point = (0.0, 0.0, self.A_beam_position - self.beam_length/2)
            self.A_beam_section.end_point = (0.0, 0.0, self.A_beam_position + self.beam_length/2)
            self.A_beam_position += self.beam_speed
            self.C_beam_section.start_point = (0.0, 0.0, self.C_beam_position + self.beam_length/2)
            self.C_beam_section.end_point = (0.0, 0.0, self.C_beam_position - self.beam_length/2)
            self.C_beam_position -= self.beam_speed
        else:
            if self.incoming:
                self.collide(0)          
            self.stop()

        for particle in self.particles:
            particle.update(dt)


        
    def start(self):
        if not self.A_beam in self.group.controllers:
            self.A_beam_position = -self.beam_start
            self.A_beam_section.start_point = (0.0, 0.0, self.A_beam_position - self.beam_length/2)
            self.A_beam_section.end_point = (0.0, 0.0, self.A_beam_position + self.beam_length/2)
            self.group.bind_controller(self.A_beam)
        if not self.C_beam in self.group.controllers:
            self.C_beam_position = self.beam_start
            self.C_beam_section.start_point = (0.0, 0.0, self.C_beam_position - self.beam_length/2)
            self.C_beam_section.end_point = (0.0, 0.0, self.C_beam_position + self.beam_length/2)
            self.group.bind_controller(self.C_beam)
        for particle in self.particles:
            particle.stop()
        self.incoming = True
            

    
    def A_stop(self):
        if self.A_beam in self.group.controllers:
            self.group.unbind_controller(self.A_beam)

    def C_stop(self):
        if self.C_beam in self.group.controllers:
            self.group.unbind_controller(self.C_beam)

    def stop(self):
        if self.incoming:
            self.A_stop()
            self.C_stop()
            for particle in self.particles:
                particle.start()
            self.incoming = False


    def collide(self,dt):
        self.collision.emit(400, self.colsparks)
