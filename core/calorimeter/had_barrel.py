import calorimeter, ring, cell
import pyglet
import math

####################################################
## Makes an EM barrel                             ##
####################################################

class HAD_Barrel(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        calorimeter.Calorimeter.__init__(self)

        self.inner_radius = 0.74
        self.outer_radius = 0.96
        self.max_abs_z    = 0.9
        self.n_z          = 7
        self.n_phi        = 12
        self.color_inner  = (0.35, 0.2, 0.1)
        self.color_outer  = (0.7, 0.4, 0.2)
        self.transparency = 0.1

        self.coalesce_first = 3.7857
        self.coalesce_last = 5.7857

        coalesce_wait = (self.coalesce_last - self.coalesce_first)/self.n_z
        
        full_delta_z = self.max_abs_z*2 / (self.n_z - 1)
        z_width = 0.9*full_delta_z
        
        for i in range(self.n_z):
            z = self.max_abs_z - i*full_delta_z

            new_ring =ring.Ring((self.inner_radius,
                                 self.outer_radius,
                                 z,
                                 z_width),
                                 self.n_phi,
                                 cell.GEO_CYLINDRICAL,
                                 self.color_inner,
                                 self.color_outer,
                                 self.transparency)

            pyglet.clock.schedule_once(new_ring.set_in_motion, self.coalesce_first + i*coalesce_wait)
            
            self.rings.append(new_ring)

        
