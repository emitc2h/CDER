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
        self.y_perspective = 0.0
        self.r_perspective = 0.0
        self.cell_phi_draw_first = 0.0


    def draw(self):

		for ring in self.rings:
			if ring.y_angle > abs(self.y_perspective):
				ring.cell_phi_draw_first = self.cell_phi_draw_first
				ring.draw()

		for ring in reversed(self.rings):
			if ring.y_angle <= abs(self.y_perspective):
				ring.cell_phi_draw_first = self.cell_phi_draw_first
				ring.draw()



            
    def update(self, dt):

        for ring in self.rings:
            ring.update(dt)        
