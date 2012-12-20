from particle import Particle

class MET():

    def __init__(self, pt, phi):

        self.pt  = pt
        self.phi = phi

        self.color = (0.0, 0.8, 0.0)

        self.particles = [Particle(self.pt,
                                   0.0,
                                   self.phi,
                                   self.color,
                                   isEM=False, 
                                   isHAD=False,
                                   is_min_ion=True)]
