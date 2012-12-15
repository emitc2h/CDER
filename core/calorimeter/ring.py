import cell
import math

####################################################
## An assemblage of cells covering all phi        ##
####################################################

class Ring():

    def __init__(self, parameters, n, geometry, color_inner, color_outer, transparency = 0.3):
        """
        Constructor
        """

        self.geometry = geometry
        
        self.radius_inner = parameters[0]
        self.radius_outer = parameters[1]
        self.z_center     = parameters[2]
        self.z_width      = parameters[3]
        self.color_inner  = color_inner
        self.color_outer  = color_outer
        self.transparency = transparency
        self.n = n
        self.cells = []

        self.generate_cells()

        
    def generate_cells(self):
        """
        Generate the cells from the parameters
        """

        full_delta_phi = 2*math.pi / float(self.n)
        phi_width = 0.9*full_delta_phi
        
        for i in range(self.n):

            phi_center = i*full_delta_phi

            new_cell = cell.Cell((self.radius_inner,
                                  self.radius_outer,
                                  self.z_center,
                                  self.z_width,
                                  phi_center,
                                  phi_width),
                                  self.geometry,
                                  self.color_inner,
                                  self.color_outer,
                                  self.transparency)

            self.cells.append(new_cell)

            
    def draw(self):
        """
        Draw the ring
        """

        for c in self.cells:
            c.draw()
            
