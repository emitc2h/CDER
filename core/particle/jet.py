from particle import Particle
import random, math

class Jet():

    def __init__(self, pt, eta, phi):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.color_charged = (0.65, 0.25, 0.0)
        self.color_neutral = (0.40, 0.45, 0.50)
        
        self.particles = []

        self.generate()
        
        
    def generate(self):
        n_max = int(4*math.log(self.pt/1000.0))
        n_charged = random.randint(2,n_max)
        n_neutral = random.randint(1,n_max-n_max/2)
        n = n_charged + n_neutral
        width = 0.2*math.exp(-self.pt/25000.0 + 1) + 0.05

        deta = 0
        dphi = 0
        
        for i in range(n):
            if i < (n-1):
                particle_eta = random.gauss(self.eta+deta, (math.exp(-float(i)/(n/3)))*width)
                particle_phi = random.gauss(self.phi+deta, (math.exp(-float(i)/(n/3)))*width)
                deta += (self.eta - particle_eta)
                dphi += (self.phi - particle_phi)
            else:
                particle_eta = self.eta + deta
                particle_phi = self.phi + dphi
                
            particle_pt  = float(self.pt)/n

            if i < n_charged:
                new_particle = Particle(particle_pt,
                                        particle_eta,
                                        particle_phi,
                                        self.color_charged,
                                        isEM=True, 
                                        isHAD=True)
            else:
                new_particle = Particle(particle_pt,
                                        particle_eta,
                                        particle_phi,
                                        self.color_neutral,
                                        isEM=True, 
                                        isHAD=False)

            self.particles.append(new_particle)
