from particle import Particle
from object import Object
import math

class MET(Object):

    def __init__(self, pt, phi):

        Object.__init__(self, pt, 0.0, phi)

        intensity = 0.01*math.log(self.pt/1000.0)
        
        self.color = (0.0, intensity, 0.0)

        self.particles.append(Particle(self.pt,
                                       0.0,
                                       self.phi,
                                       self.color,
                                       isEM=False, 
                                       isHAD=False,
                                       is_min_ion=False,
                                       wide=True))
