import cell
import math

####################################################
## A simple polyhedron with 8 faces that serves   ##
## as the basic calorimeter cell. Arrange several ##
## of these to determine calormeter geometry      ##
####################################################

class Ring():

    def __init__(self, parameters, n, geometry):
        """
        Constructor
        """

        self.geometry = geometry
        
        self.radius_inner = parameters[0]
        self.radius_outer = parameters[1]
        self.z_center     = parameters[2]
        self.z_width       = parameters[3]
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
                                  self.geometry)

            self.cells.append(new_cell)

            
    def draw(self):
        """
        Draw the ring
        """

        for c in self.cells:
            c.draw()
            
