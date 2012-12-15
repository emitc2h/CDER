import calorimeter, ring, cell
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
        self.n_phi        = 16
        self.color_inner  = (0.35, 0.2, 0.1)
        self.color_outer  = (0.7, 0.4, 0.2)
        self.transparency = 0.1

        full_delta_z = self.max_abs_z*2 / (self.n_z - 1)
        z_width = 0.9*full_delta_z
        
        for i in range(self.n_z):
            z = self.max_abs_z - i*full_delta_z

            self.rings.append(ring.Ring((self.inner_radius,
                                         self.outer_radius,
                                         z,
                                         z_width),
                                         self.n_phi,
                                         cell.GEO_CYLINDRICAL,
                                         self.color_inner,
                                         self.color_outer,
                                         self.transparency))

        
