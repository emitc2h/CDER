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
        self.reverse_draw_order = False
        self.cell_phi_draw_first = 0.0


    def draw(self):

        if self.reverse_draw_order:
            for ring in reversed(self.rings):
                ring.cell_phi_draw_first = self.cell_phi_draw_first
                ring.draw()
        else:
            for ring in self.rings:
                ring.cell_phi_draw_first = self.cell_phi_draw_first
                ring.draw()

            
    def update(self, dt):

        for ring in self.rings:
            ring.update(dt)        
