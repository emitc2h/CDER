#**************************************************#
# file   : core/calorimeter/em.py                  #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A simple EM calorimeter with projective          #
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
from ..utils import eta_to_z
from ..config import *

####################################################
class EM_Calorimeter(calorimeter.Calorimeter):

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
        self.calo_type = calorimeter.CALO_EM
        
        
        ## Barrel parameters
        self.barrel_inner_radius = em_inner_radius 
        self.barrel_outer_radius = em_outer_radius 
        self.barrel_max_abs_eta  = em_max_abs_eta  
        self.barrel_n_eta        = em_eta_divisions
        self.barrel_n_phi        = em_phi_divisions

        
        ## Endcaps parameters
        self.endcap_inner_radius = 0.20*self.barrel_inner_radius
        self.endcap_outer_radius = 0.95*self.barrel_inner_radius
        self.endcap_max_abs_z    = eta_to_z((self.barrel_outer_radius, self.barrel_max_abs_eta))
        self.endcap_z_width      = em_endcap_thickness*self.endcap_max_abs_z
        self.endcap_n_phi        = self.barrel_n_phi

        
        ## Aspect, color and opacity
        self.inner_color  = (0.1, 0.2, 0.35)
        self.outer_color  = (0.2, 0.4, 0.7)
        self.opacity = 0.05

        
        ## Calorimeter construction animation timing
        self.construct_A_side = 0.0
        self.construct_first = 0.2857
        self.construct_last = 2.2857
        self.construct_C_side = 1.8

        construct_wait = (self.construct_last - self.construct_first)/self.barrel_n_eta



        ## A endcap ring ##
        #-----------------#
        
        ## Instantiate A-side endcap ring
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
        
        ## Figure out eta width and divisions of barrel rings
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
                                  self.inner_color,
                                  self.outer_color,
                                  self.opacity)

            ## Set barrel rings in motion from A-side to C-side
            pyglet.clock.schedule_once(new_ring.set_in_motion, self.construct_first + i*construct_wait)
            
            self.rings.append(new_ring)



        ## C endcap ring ##
        #-----------------#

        ## Instantiate C-side endcap ring
        C_ring = ring.Ring((self.endcap_inner_radius,
							self.endcap_outer_radius,
							-self.endcap_max_abs_z,
							self.endcap_z_width),
							self.endcap_n_phi,
							cell.GEO_CYLINDRICAL,
							self.inner_color,
							self.outer_color,
							self.opacity)

        ## C-ring is set in motion before last barrel ring (endcap inside the barrel)
        pyglet.clock.schedule_once(C_ring.set_in_motion, self.construct_C_side)

        self.rings.append(C_ring)

        
