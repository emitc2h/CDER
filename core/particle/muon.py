#**************************************************#
# file   : core/particle/jet.py                    #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A muon                                           #
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

## CDER imports
from particle import Particle
from object import Object

####################################################
class Muon(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, eta, phi)

        ## Muon is crimson
        self.color = (0.6, 0.0, 0.2)

        ## Electron is a single minimum ionizing particle
        ## (makes it through the calorimeter)
        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=False, 
                                   isHAD=False,
                                   is_min_ion=True)]
