from particle import Particle
from object import Object

class MET(Object):

    def __init__(self, pt, phi):

        Object.__init__(self, pt, 0.0, phi)

        self.color = (0.0, 0.8, 0.0)

        for eta in range(-10, 10):
            self.particles.append(Particle(self.pt,
                                   eta*0.02,
                                   self.phi,
                                   self.color,
                                   isEM=False, 
                                   isHAD=False,
                                   is_min_ion=False))
