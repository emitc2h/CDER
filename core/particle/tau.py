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
class Tau(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, eta, phi)

        ## Define colors for charged and neutral particles
        self.color_charged = (0.45, 0.45, 0.00)
        self.color_neutral = (0.40, 0.45, 0.50)

        # Generate the decay products
        self.generate()
        

        
    ## --------------------------------------- ##
    def generate(self):
        """
        Generate the tau decay products
        """

        ## Pick hadronic decay ##
        #-----------------------#

        ## Normalize probability to get rid of leptonic decays
        decay = random.random()*0.6051
        n_charged=0
        n_neutral=0

        ## Select one of the 6 most common hadronic decays
        ## (in order of likelihood)
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

        ## Set tau width according to tau Pt
        width = 0.049*math.exp(-self.pt/25000.0 + 1) + 0.01
        n = n_charged + n_neutral

        ## Make sure decay products Eta and Phi sum up to tau Eta and Phi
        deta = 0
        dphi = 0

        ## Generate specific decay products
        for i in range(n):

            ## Randomly generate eta and phi for n-1 first decay products,
            ## new particles eta and phi become incresingly constrained as new
            ## particles are added
            if i < (n-1):
                particle_eta = random.gauss(self.eta+deta, (float(n-i)/n)*width)
                particle_phi = random.gauss(self.phi+deta, (float(n-i)/n)*width)
                deta += (self.eta - particle_eta)
                dphi += (self.phi - particle_phi)

            ## Make sure the last particle balances all the other
            else:
                particle_eta = self.eta + deta
                particle_phi = self.phi + dphi

            # Distribute Pt equally among decay products
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
                
