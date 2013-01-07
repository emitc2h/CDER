#**************************************************#
# file   : core/calorimeter/had.py                 #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A simple HAD calorimeter with cylindrical        #
# geometry                                         #
#**************************************************#

#############################################################################
#   Copyright 2012-2013 Michel Trottier-McDonald                            #
#                                                                           #
#   This file is part of CDER.                                              #
#                                                                           #
#   CDER is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   CDER is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
#############################################################################

## Pyglet imports
import pyglet

## Basic python imports
import math

## CDER imports
import calorimeter, ring, cell
from ..config import *

####################################################
class HAD_Calorimeter(calorimeter.Calorimeter):

    ## --------------------------------------- ##
    def __init__(self):
        """
        Constructor
        """

        ## Base class constructor
        calorimeter.Calorimeter.__init__(self)



        ## Calorimeter configuration ##
        #-----------------------------#

        ## Calorimeter type
        self.calo_type = calorimeter.CALO_HAD

        
        ## Barrel parameters
        self.barrel_inner_radius = had_inner_radius 
        self.barrel_outer_radius = had_outer_radius 
        self.barrel_max_abs_z    = had_max_abs_z
        self.barrel_n_z          = had_eta_divisions
        self.barrel_n_phi        = had_phi_divisions


        ## Figure out eta width and divisions of rings
        full_delta_z = self.barrel_max_abs_z*2 / (self.barrel_n_z - 1)
        z_width = 0.9*full_delta_z

        
        ## Endcap parameters
        self.endcap_inner_radius = 0.20*self.barrel_inner_radius
        self.endcap_outer_radius = self.barrel_outer_radius
        self.endcap_max_abs_z    = self.barrel_max_abs_z + full_delta_z
        self.endcap_z_width      = z_width
        self.endcap_n_phi        = self.barrel_n_phi


        ## Aspect, color and opacity
        self.inner_color  = (0.35, 0.2, 0.1)
        self.outer_color  = (0.7, 0.4, 0.2)
        self.opacity = 0.05

        
        ## Coalescing calorimeter animation timing
        self.construct_A_side = 3.5
        self.construct_first = 3.7857
        self.construct_last = 5.7857
        self.construct_C_side = 6.0

        construct_wait = (self.construct_last - self.construct_first)/self.barrel_n_z



        ## A endcap ring ##
        #-----------------#

        ## Instantiate A-side ring
        A_ring = ring.Ring((self.endcap_inner_radius,
                            self.endcap_outer_radius,
                            self.endcap_max_abs_z,
                            self.endcap_z_width),
                            self.endcap_n_phi,
                            cell.GEO_CYLINDRICAL,
                            self.inner_color,
                            self.outer_color,
                            self.opacity)

        ## A-ring is the first to be constructed
        pyglet.clock.schedule_once(A_ring.set_in_motion, self.construct_A_side)

        self.rings.append(A_ring)



        ## Barrel rings ##
        #----------------#
        
        for i in range(self.barrel_n_z):
            z = self.barrel_max_abs_z - i*full_delta_z

            ## Separate barrel and extended barrels
            if i==2 or i==7: continue

            new_ring =ring.Ring((self.barrel_inner_radius,
                                 self.barrel_outer_radius,
                                 z,
                                 z_width),
                                 self.barrel_n_phi,
                                 cell.GEO_CYLINDRICAL,
                                 self.inner_color,
                                 self.outer_color,
                                 self.opacity)

            ## Set barrel rings in motion from A-side to C-side
            pyglet.clock.schedule_once(new_ring.set_in_motion, self.construct_first + i*construct_wait)
            
            self.rings.append(new_ring)


        ## Instantiate C-side ring
        C_ring = ring.Ring((self.endcap_inner_radius,
                            self.endcap_outer_radius,
                            -self.endcap_max_abs_z,
                            self.endcap_z_width),
                            self.endcap_n_phi,
                            cell.GEO_CYLINDRICAL,
                            self.inner_color,
                            self.outer_color,
                            self.opacity)

        ## A-ring is the last to be constructed
        pyglet.clock.schedule_once(C_ring.set_in_motion, self.construct_C_side)

        self.rings.append(C_ring)
