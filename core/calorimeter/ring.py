#**************************************************#
# file   : core/calorimeter/ring.py                #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# An arrangement of n cells distributed equally on #
# a ring in phi                                    #
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

## Basic python imports
from itertools import cycle, islice, dropwhile
import math

## CDER imports
import cell
from ..utils import delta_phi, inabspi

####################################################
class Ring():

    ## --------------------------------------- ##
    def __init__(self, parameters, n, geometry, inner_color, outer_color, opacity = 0.3):
        """
        Constructor
        """

        ## Check that a 4-tuple is provided
        n_parameters = len(parameters)
        if n_parameters != 4:
            raise ValueError('There should be 4 parameters to define the ring. Only %d provided.' % n_parameters)

        ## Specify cell geometry
        self.geometry = geometry

        ## Set geometry parameters
        self.inner_radius = parameters[0]
        self.outer_radius = parameters[1]
        self.z_center     = parameters[2]
        self.z_width      = parameters[3]

        ## Color gradient from inside to outside
        self.outer_color = outer_color
        self.inner_color = inner_color

        ## Cell opacity (also serves to display cell energy)
        self.opacity = opacity

        ## ring construction Animation
        self.in_motion = False
        self.distance = 100.0

        ## Draw order according to camera position in case
        ## of disabled depth test
        self.phi_camera = 0.0

        if abs(self.z_center) < 1e-10:
            self.y_angle  = 0.0
        else:
            self.y_angle  = math.atan2(self.z_center-self.z_width/2,
                                       self.outer_radius)

        ## Cell arangement
        self.n = n
        self.cells = []

        ## Generate the cells according to the specified arrangement
        self.generate_cells()

        

    ## --------------------------------------- ##
    def generate_cells(self):
        """
        Generate the cells from the parameters
        """

        ## Determine spacing between cells in phi
        full_delta_phi = 2*math.pi / float(self.n)
        self.phi_width = 0.9*full_delta_phi

        ## Create the cells
        for i in range(self.n):
            phi_center = i*full_delta_phi

            new_cell = cell.Cell((self.inner_radius,
                                  self.outer_radius,
                                  self.z_center,
                                  self.z_width,
                                  phi_center,
                                  self.phi_width),
                                  self.geometry,
                                  self.inner_color,
                                  self.outer_color,
                                  self.opacity)

            self.cells.append(new_cell)

            

    ## --------------------------------------- ##
    def update(self, dt):
        """
        Manage ring construction animation
        """
        
        if not self.in_motion:
            return

        ## Reduce cell distance
        self.distance -= 1.0*(math.log(1.001+0.2*self.distance))

        ## Once cells are at the final position, terminate animation
        if self.distance < 0.0:
            self.distance = 0.0
            self.in_motion = False


            
    ## --------------------------------------- ##
    def set_in_motion(self, dt):
        """
        Begin ring construction animation
        """
        
        self.distance = 10.0
        self.in_motion = True
    


    ## --------------------------------------- ##
    def draw(self):
        """
        Draw the ring
        """

        ## Cycle the list of cells to begin with the cell opposite to the camera
        cell_iterator = cycle(self.cells)
        cell_iterator = dropwhile(lambda cell: delta_phi(cell.phi_center, self.phi_camera) > cell.phi_width,
								  cell_iterator)
        cell_iterator = islice(cell_iterator, None, self.n)
        ordered_cells = list(cell_iterator)

        ## Draw cells
        for i in range(self.n):
            ## Alternate clockwise and anti-clockwise
            a = (i+1)/2
            if i%2 > 0:
                a = -a
            ordered_cells[a].distance = self.distance
            ordered_cells[a].draw()
