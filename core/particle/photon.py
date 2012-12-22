from particle import Particle
from object import Object

class Photon(Object):

    def __init__(self, pt, eta, phi):

        Object.__init__(self, pt, eta, phi)

        self.color = (0.40, 0.45, 0.50)

        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
