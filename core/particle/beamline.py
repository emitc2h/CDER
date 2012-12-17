import os
import math
import time
from pyglet import image
from pyglet.gl import *

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender

class Beamline():

    def __init__(self):
        
        self.spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'flare3.png')).get_texture()

        self.sparks = ParticleGroup(
            controllers=[
                Lifetime(3),
                Movement(damping=0.93),
                Fader(fade_out_start=0.75, fade_out_end=3.0),
                ],
            renderer=BillboardRenderer(SpriteTexturizer(self.spark_tex.id)))

        self.spark_emitter = StaticEmitter(
            template=Particle(
                position=(0,0,0), 
                color=(1,1,1), 
                size=(0.06,0.06,0)),
            deviation=Particle(
                position=(0.03,0.03,0.03), 
                velocity=(2.25,2.25,2.25), 
                size=(0.006,0.006,0),
                age=1.5))

        self.fire_tex = image.load(os.path.join(os.path.dirname(__file__), 'puff.png')).get_texture()

        self.fire = ParticleGroup(
            controllers=[
                Lifetime(4),
                Movement(damping=0.95),
                Fader(fade_in_start=0, start_alpha=0, fade_in_end=0.5, max_alpha=0.4, 
                      fade_out_start=1.0, fade_out_end=4.0)
                      ],
                renderer=BillboardRenderer(SpriteTexturizer(self.fire_tex.id)))

        self.fire_emitter = StaticEmitter(
            template=Particle(
                position=(0,0,0), 
                size=(0.6,0.6,0)),
            deviation=Particle(
                position=(0.06,0.06,0.06), 
                velocity=(0.6,0.6,0.6), 
                size=(0.15,0.15,0),
                up=(0,0,math.pi*2), 
                rotation=(0,0,math.pi*0.03),),
                color=[(0.5,0,0), (0.5,0.5,0.5), (0.4,0.1,0.1), (0.85,0.3,0)],
            )

    def explode(self):
        self.fire_emitter.emit(400, self.fire)
        self.spark_emitter.emit(400, self.sparks)
    
