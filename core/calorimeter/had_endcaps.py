import calorimeter, ring, cell
import math

####################################################
## Makes both HAD endcaps                         ##
####################################################

class HAD_Endcaps(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        calorimeter.Calorimeter.__init__(self)

        self.inner_radius = 0.26
        self.outer_radius = 0.96
        self.max_abs_z    = 1.2
        self.z_width      = 0.2
        self.n_phi        = 16
        self.color_inner  = (0.35, 0.2, 0.1)
        self.color_outer  = (0.7, 0.4, 0.2)
        self.transparency = 0.1

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
