import calorimeter, ring, cell
import math

####################################################
## Makes both EM endcaps                          ##
####################################################

class EM_Endcaps(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        calorimeter.Calorimeter.__init__(self)

        self.inner_radius = 0.16
        self.outer_radius = 0.56
        self.max_abs_z    = 0.9
        self.z_width      = 0.2
        self.n_phi        = 8
        self.color_inner  = (0.1, 0.2, 0.35)
        self.color_outer  = (0.2, 0.4, 0.7)
        self.transparency = 0.3

        self.rings.append(ring.Ring((self.inner_radius,
                                     self.outer_radius,
                                     self.max_abs_z,
                                     self.z_width),
                                    self.n_phi,
                                    cell.GEO_CYLINDRICAL,
                                    self.color_inner,
                                    self.color_outer,
                                    self.transparency))

        self.rings.append(ring.Ring((self.inner_radius,
                                     self.outer_radius,
                                     -self.max_abs_z,
                                     self.z_width),
                                    self.n_phi,
                                    cell.GEO_CYLINDRICAL,
                                    self.color_inner,
                                    self.color_outer,
                                    self.transparency))
