import calorimeter, ring, cell
import pyglet
import math

####################################################
## Makes an EM barrel                             ##
####################################################

class EM_Calorimeter(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        ## Initiate parent class
        calorimeter.Calorimeter.__init__(self)

        
        ## Barrel parameters
        self.barrel_inner_radius = 1.5
        self.barrel_outer_radius = 1.95
        self.barrel_max_abs_eta  = 1.475
        self.barrel_n_eta        = 14
        self.barrel_n_phi        = 30

        
        ## Endcaps parameters
        self.endcap_inner_radius = 0.4
        self.endcap_outer_radius = 1.4
        self.endcap_max_abs_z    = 4.3
        self.endcap_z_width      = 0.6
        self.endcap_n_phi        = 30

        
        ## Aspect, color and transparency
        self.color_inner  = (0.1, 0.2, 0.35)
        self.color_outer  = (0.2, 0.4, 0.7)
        self.transparency = 0.1

        
        ## Coalescing calorimeter animation timing
        self.coalesce_A_side = 0.0
        self.coalesce_first = 0.2857
        self.coalesce_last = 2.2857
        self.coalesce_C_side = 1.8

        coalesce_wait = (self.coalesce_last - self.coalesce_first)/self.barrel_n_eta

        
        ## Instantiate A-side endcap ring
        A_ring = ring.Ring((self.endcap_inner_radius,
							self.endcap_outer_radius,
							self.endcap_max_abs_z,
							self.endcap_z_width),
							self.endcap_n_phi,
							cell.GEO_CYLINDRICAL,
							self.color_inner,
							self.color_outer,
							self.transparency)

        pyglet.clock.schedule_once(A_ring.set_in_motion, self.coalesce_A_side)

        self.rings.append(A_ring)

        
        ## Instantiate barrel rings
        full_delta_eta = self.barrel_max_abs_eta*2 / (self.barrel_n_eta - 1)
        eta_width = 0.8*full_delta_eta
        
        for i in range(self.barrel_n_eta):
            eta = self.barrel_max_abs_eta - i*full_delta_eta

            new_ring = ring.Ring((self.barrel_inner_radius,
                                  self.barrel_outer_radius,
                                  eta,
                                  eta_width),
                                  self.barrel_n_phi,
                                  cell.GEO_PROJECTIVE,
                                  self.color_inner,
                                  self.color_outer,
                                  self.transparency)

            pyglet.clock.schedule_once(new_ring.set_in_motion, self.coalesce_first + i*coalesce_wait)
            
            self.rings.append(new_ring)


        ## Instantiate A-side endcap ring
        C_ring = ring.Ring((self.endcap_inner_radius,
							self.endcap_outer_radius,
							-self.endcap_max_abs_z,
							self.endcap_z_width),
							self.endcap_n_phi,
							cell.GEO_CYLINDRICAL,
							self.color_inner,
							self.color_outer,
							self.transparency)

        pyglet.clock.schedule_once(C_ring.set_in_motion, self.coalesce_C_side)

        self.rings.append(C_ring)

        
