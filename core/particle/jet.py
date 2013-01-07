#**************************************************#
# file   : core/particle/jet.py                    #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A jet                                            #
#**************************************************#

#############################################################################
#   Copyright 2012-2013 Michel Trottier-McDonald                            #
#                                                                           #
#   This file is part of CDER.                                              #
#                                                                           #
#   CDER is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   CDER is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
#############################################################################

## Basic python imports
import random, math

## CDER imports
from particle import Particle
from object import Object

####################################################
class Jet(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi, btag=False):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, eta, phi)

        ## Define colors for charged and neutral particles
        self.color_charged = (0.65, 0.25, 0.0)
        self.color_neutral = (0.40, 0.45, 0.50)

        ## Is it a b-tagged jet
        self.btag = btag

        ## Generate the particles making the jet
        self.generate()
        

        
    ## --------------------------------------- ##
    def generate(self):
        """
        Generate the particles making the jet
        """

        ## Number of particles go with jet Pt (approximate)
        n_max = int(math.log(self.pt/1000.0 + 1.0))

        ## At least two charged particles
        n_charged = random.randint(2,n_max)

        ## Random number of neutral particles
        n_neutral = random.randint(1,n_max-n_max/2)

        ## Effective number of particles
        n = n_charged + n_neutral

        ## jet width determined by jet Pt (approximate collimation effect)
        width = 0.2*math.exp(-self.pt/25000.0 + 1) + 0.05

        ## Make sure jet particles Eta and Phi sum up to jet Eta and Phi
        deta = 0
        dphi = 0

        ## Generate specific jet particles
        for i in range(n):

            ## Randomly generate eta and phi for n-1 first jet particles,
            ## new particles eta and phi become incresingly constrained as new
            ## particles are added
            if i < (n-1):
                particle_eta = random.gauss(self.eta+deta, (math.exp(-float(i)/(n/3)))*width)
                particle_phi = random.gauss(self.phi+deta, (math.exp(-float(i)/(n/3)))*width)
                deta += (self.eta - particle_eta)
                dphi += (self.phi - particle_phi)

            ## Make sure the last particle balances all the other
            else:
                particle_eta = self.eta + deta
                particle_phi = self.phi + dphi

            ## Distribute Pt equally among decay products
            particle_pt  = float(self.pt)/n

            ## First particles are charged
            if i < n_charged:
                new_particle = Particle(particle_pt,
                                        particle_eta,
                                        particle_phi,
                                        self.color_charged,
                                        isEM=True, 
                                        isHAD=True)

            ## The rest are neutral
            else:
                new_particle = Particle(particle_pt,
                                        particle_eta,
                                        particle_phi,
                                        self.color_neutral,
                                        isEM=True, 
                                        isHAD=False)

            self.particles.append(new_particle)

        ## Add b-tag beam if the jet is b-tagged
        if self.btag:
            new_particle = Particle(self.pt,
                                    self.eta,
                                    self.phi,
                                    (0.0, 0.06, 0.06),
                                    isEM=True, 
                                    isHAD=True,
                                    wide=True)

            self.particles.append(new_particle)
            
