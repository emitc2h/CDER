#**************************************************#
# file   : core/particle/jet.py                    #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A muon                                           #
#**************************************************#

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
