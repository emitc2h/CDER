import calorimeter, ring, cell
import pyglet
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
        self.max_abs_z    = 0.8
        self.z_width      = 0.2
        self.n_phi        = 6
        self.color_inner  = (0.1, 0.2, 0.35)
        self.color_outer  = (0.2, 0.4, 0.7)
        self.transparency = 0.3

        self.coalesce_A = 0.0
        self.coalesce_C = 1.6
        
        A_ring = ring.Ring((self.inner_radius,
							self.outer_radius,
							self.max_abs_z,
							self.z_width),
							self.n_phi,
							cell.GEO_CYLINDRICAL,
							self.color_inner,
							self.color_outer,
							self.transparency)

        pyglet.clock.schedule_once(A_ring.set_in_motion, self.coalesce_A)
		
        C_ring = ring.Ring((self.inner_radius,
							self.outer_radius,
							-self.max_abs_z,
							self.z_width),
							self.n_phi,
							cell.GEO_CYLINDRICAL,
							self.color_inner,
							self.color_outer,
							self.transparency)
		
        pyglet.clock.schedule_once(C_ring.set_in_motion, self.coalesce_C)
        
        self.rings = [A_ring, C_ring]
