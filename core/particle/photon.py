#**************************************************#
# file   : core/particle/photon.py                 #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A photon                                         #
#**************************************************#

## CDER imports
from particle import Particle
from object import Object

####################################################
class Photon(Object):

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi):
        """
        Constructor
        """

        ## Base class constructor
        Object.__init__(self, pt, eta, phi)

        ## Photon is white/blueish
        self.color = (0.40, 0.45, 0.50)

        ## Photon is a single particle
        self.particles = [Particle(self.pt,
                                   self.eta,
                                   self.phi,
                                   self.color,
                                   isEM=True, 
                                   isHAD=False)]
