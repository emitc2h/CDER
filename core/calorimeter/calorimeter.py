import math

####################################################
## An assemblage of rings making a calorimeter    ##
## component                                      ##
####################################################

class Calorimeter():

    def __init__(self):
        """
        Constructor
        """

        self.rings = []


    def draw(self):

        for ring in self.rings:
            ring.draw()
        
