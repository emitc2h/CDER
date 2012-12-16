import cell
from ..utils import delta_phi, inabspi
from itertools import cycle, islice, dropwhile
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
        self.y_angle      = math.atan2(self.z_center/9, self.radius_inner) + math.pi/2
        self.color_inner  = color_inner
        self.color_outer  = color_outer
        self.transparency = transparency
        self.in_motion = False
        self.distance = 100.0
        self.cell_phi_draw_first = 0.0
        self.n = n
        self.cells = []

        self.generate_cells()

        
    def generate_cells(self):
        """
        Generate the cells from the parameters
        """

        full_delta_phi = 2*math.pi / float(self.n)
        self.phi_width = 0.9*full_delta_phi

        for i in range(self.n):
				
            phi_center = i*full_delta_phi

            new_cell = cell.Cell((self.radius_inner,
                                  self.radius_outer,
                                  self.z_center,
                                  self.z_width,
                                  phi_center,
                                  self.phi_width),
                                  self.geometry,
                                  self.color_inner,
                                  self.color_outer,
                                  self.transparency)

            self.cells.append(new_cell)


    def update(self, dt):
        if not self.in_motion:
            return
        self.distance -= 1.0*(math.log(1.001+0.2*self.distance))
        if self.distance < 0.0:
            self.distance = 0.0
            self.in_motion = False


    def set_in_motion(self, dt):
        self.distance = 10.0
        self.in_motion = True
    
            
    def draw(self):
        """
        Draw the ring
        """

        cell_iterator = cycle(self.cells)
        cell_iterator = dropwhile(lambda cell: delta_phi(cell.phi_center, self.cell_phi_draw_first) > cell.phi_width,
								  cell_iterator)
        cell_iterator = islice(cell_iterator, None, self.n)

        ordered_cells = list(cell_iterator)
        
        for i in range(self.n):
            ## Figure out order of creation for transparency
            a = (i+1)/2
            if i%2 > 0:
                a = -a
            ordered_cells[a].distance = self.distance
            ordered_cells[a].draw()
