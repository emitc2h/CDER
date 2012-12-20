from particle import Particle
import random, math

class Tau():

    def __init__(self, pt, eta, phi):

        self.pt  = pt
        self.eta = eta
        self.phi = phi

        self.color_charged = (0.65, 0.45, 0.00)
        self.color_neutral = (0.40, 0.45, 0.50)
        
        self.particles = []

        self.generate()
        

    def generate(self):

        ## Randomly generate hadronic tau decay
        decay = random.random()*0.6051
        n_charged=0
        n_neutral=0
        if decay < 0.2531:
            n_charged=1
            n_neutral=1
        elif decay < 0.3638:
            n_charged=1
            n_neutral=0
        elif decay < 0.4585:
            n_charged=3
            n_neutral=0
        elif decay < 0.5506:
            n_charged=1
            n_neutral=2
        elif decay < 0.5929:
            n_charged=3
            n_neutral=1
        elif decay < 0.6051:
            n_charged=1
            n_neutral=3

        width = 0.049*math.exp(-self.pt/25000.0 + 1) + 0.01
        n = n_charged + n_neutral

        deta = 0
        dphi = 0
        
        for i in range(n):
            if i < (n-1):
                particle_eta = random.gauss(self.eta+deta, (float(n-i)/n)*width)
                particle_phi = random.gauss(self.phi+deta, (float(n-i)/n)*width)
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
                
