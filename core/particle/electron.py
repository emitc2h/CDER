#**************************************************#
# file   : core/particle/electron.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# An electron                                      #
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
class Electron(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, eta, phi)

        ## Electron is blue
        self.color = (0.1, 0.1, 1.0)

        ## Electron is a single particle
        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
