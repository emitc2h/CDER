#**************************************************#
# file   : core/particle/met.py                    #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# MET                                              #
#**************************************************#

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
        intensity = 0.01*math.log(self.pt/1000.0)

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
