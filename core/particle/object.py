#**************************************************#
# file   : core/particle/object.py                 #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A simple base class making sure that every       #
# object displayed in CDER has basic kinematics    #
# and a list of particles to display               #
#**************************************************#

####################################################
class Object():

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi):
        """
        Constructor
        """

        ## Basic kinematics
        self.pt  = pt
        self.eta = eta
        self.phi = phi

        ## Particle list
        self.particles = []
