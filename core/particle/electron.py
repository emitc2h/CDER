#**************************************************#
# file   : core/particle/electron.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# An electron                                      #
#**************************************************#

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
