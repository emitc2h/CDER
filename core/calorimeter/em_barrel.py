import calorimeter, ring, cell
import math

####################################################
## Makes an EM barrel                             ##
####################################################

class EM_Barrel(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        calorimeter.Calorimeter.__init__(self)

        self.inner_radius = 0.6
        self.outer_radius = 0.7
        self.max_abs_eta  = 0.9
        self.n_eta        = 7
        self.n_phi        = 16
        self.color_inner  = (0.1, 0.2, 0.35)
        self.color_outer  = (0.2, 0.4, 0.7)
        self.transparency = 0.3

        full_delta_eta = self.max_abs_eta*2 / (self.n_eta - 1)
        eta_width = 0.8*full_delta_eta
        
        for i in range(self.n_eta):
            eta = self.max_abs_eta - i*full_delta_eta

            self.rings.append(ring.Ring((self.inner_radius,
                                         self.outer_radius,
                                         eta,
                                         eta_width),
                                         self.n_phi,
                                         cell.GEO_PROJECTIVE,
                                         self.color_inner,
                                         self.color_outer,
                                         self.transparency))

        
