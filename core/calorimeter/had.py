import calorimeter, ring, cell
import pyglet
import math

####################################################
## Makes an EM barrel                             ##
####################################################

class HAD_Calorimeter(calorimeter.Calorimeter):

    def __init__(self):
        """
        Constructor
        """

        ## Initiate parent class
        calorimeter.Calorimeter.__init__(self)


        ## Barrel parameters
        self.barrel_inner_radius = 0.74
        self.barrel_outer_radius = 0.96
        self.barrel_max_abs_z    = 0.9
        self.barrel_n_z          = 7
        self.barrel_n_phi        = 12


        ## Endcap parameters
        self.endcap_inner_radius = 0.26
        self.endcap_outer_radius = 0.96
        self.endcap_max_abs_z    = 1.2
        self.endcap_z_width      = 0.2
        self.endcap_n_phi        = 6


        ## Aspect, color and transparency
        self.color_inner  = (0.35, 0.2, 0.1)
        self.color_outer  = (0.7, 0.4, 0.2)
        self.transparency = 0.1

        
        ## Coalescing calorimeter animation timing
        self.coalesce_A_side = 3.5
        self.coalesce_first = 3.7857
        self.coalesce_last = 5.7857
        self.coalesce_C_side = 6.0

        coalesce_wait = (self.coalesce_last - self.coalesce_first)/self.barrel_n_z


        ## Instantiate A-side ring
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
        full_delta_z = self.barrel_max_abs_z*2 / (self.barrel_n_z - 1)
        z_width = 0.9*full_delta_z
        
        for i in range(self.barrel_n_z):
            z = self.barrel_max_abs_z - i*full_delta_z

            new_ring =ring.Ring((self.barrel_inner_radius,
                                 self.barrel_outer_radius,
                                 z,
                                 z_width),
                                 self.barrel_n_phi,
                                 cell.GEO_CYLINDRICAL,
                                 self.color_inner,
                                 self.color_outer,
                                 self.transparency)

            pyglet.clock.schedule_once(new_ring.set_in_motion, self.coalesce_first + i*coalesce_wait)
            
            self.rings.append(new_ring)


        ## Instantiate C-side ring
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
