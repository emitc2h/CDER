from particle import Particle

class Muon():

    def __init__(self, pt, eta, phi):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.color = (0.6, 0.0, 0.2)

        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=False, 
                                   isHAD=False,
                                   is_min_ion=True)]
