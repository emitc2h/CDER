from particle import Particle

class Photon():

    def __init__(self, pt, eta, phi):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.color = (0.40, 0.45, 0.50)

        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
