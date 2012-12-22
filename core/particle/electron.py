from particle import Particle
from object import Object

class Electron(Object):

    def __init__(self, pt, eta, phi):

        Object.__init__(self, pt, eta, phi)

        self.color = (0.1, 0.1, 1.0)

        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
