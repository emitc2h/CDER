#**************************************************#
# file   : core/particle/met.py                    #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# MET                                              #
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
import math

## CDER imports
from particle import Particle
from object import Object

####################################################
class MET(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, phi):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, 0.0, phi)

        ## Brightness of the MET beam goes with MET magnitude
        intensity = 0.01*math.log(self.pt/1000.0 + 1.0)

        ## MET is green
        self.color = (0.0, intensity, 0.0)

        ## MET is made of the one beam
        self.particles.append(Particle(self.pt,
                                       0.0,
                                       self.phi,
                                       self.color,
                                       isEM=False, 
                                       isHAD=False,
                                       is_min_ion=False,
                                       wide=True))
