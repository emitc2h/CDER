from particle import Particle

class Electron():

    def __init__(self, pt, eta, phi):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.color = (0.1, 0.1, 1.0)

        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
