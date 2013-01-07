#**************************************************#
# file   : core/calorimeter/calorimeter.py         #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# An assemblage of rings making a calorimeter      #
# component                                        #
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
import math

## Default strings for calorimeter types
CALO_EM  = 'em'
CALO_HAD = 'had'

####################################################
class Calorimeter():

    ## --------------------------------------- ##
    def __init__(self):
        """
        Constructor
        """

        ## Rings making the calorimeter
        self.rings = []

        ## Default cell opacity
        self.opacity = 0.1

        ## Cells with modified opacity
        self.modified_cells = []

        ## Knowledge of camera position to determine in which order to draw the rings
        self.theta_camera = 0.0
        self.r_camera = 0.0
        self.phi_camera = 0.0

        ## Calorimeter type
        self.calo_type = None



    ## --------------------------------------- ##
    def draw(self):
        """
        Draw calorimeter rings according to camera position
        """

        ## Calculate the perspective y angle with respect to transverse plane
        a = abs(self.theta_camera)-math.pi/2

        ## Draw negative side rings
        for ring in self.rings:

            ## Find out where the camera is looking at in a perpendicular direction to the beamline
            split_angle = math.atan2(ring.outer_radius,
                                     -self.r_camera*math.sin(a)) - math.pi/2

            ## Draw all rings after that point
            if ring.y_angle > split_angle:
                ring.phi_camera = self.phi_camera
                ring.draw()

        ## Draw negative side rings
        for ring in reversed(self.rings):

            ## Find out where the camera is looking at in a perpendicular direction to the beamline
            split_angle = math.atan2(ring.outer_radius,
                                     -self.r_camera*math.sin(a)) - math.pi/2

            ## Draw all rings before that point
            if ring.y_angle < split_angle:
                ring.phi_camera = self.phi_camera
                ring.draw()

        ## If looking straight in the middle, draw the middle ring at the end
        n_rings = len(self.rings)
        if a == 0.0 and n_rings%2 > 0:
            self.rings[n_rings/2].draw()



    ## --------------------------------------- ##
    def update(self, dt):
        """
        Update rings for calorimeter construction animation
        """

        for ring in self.rings:
            ring.update(dt)



    ## --------------------------------------- ##
    def energize(self, particles):
        """
        Modify opacity of cells receiving energy from particles
        """

        ## Iterate over particles
        for particle in particles:

            ## Check that the particle hasn't hit the calorimeters it affects yet
            if not particle.is_travelling and \
              (not (particle.calo_hit_EM and self.calo_type == CALO_EM) or \
              not (particle.calo_hit_HAD and self.calo_type == CALO_HAD)):

                ## Cells to be modified by the current particle
                target_cells = []

                ## Identify cells targetted by particles
                for ring in self.rings:
                    for cell in ring.cells:
                        if particle.isEM and self.calo_type == CALO_EM or \
                          particle.isHAD and self.calo_type == CALO_HAD:
                            ## Collect endcap cells that have to be rebuilt
                            if particle.in_endcap:
                                dphi = particle.dphi(cell)
                                if particle.r < cell.outer_radius and particle.r > cell.inner_radius and \
                                  dphi < cell.phi_width/1.8 and particle.eta*cell.eta_center > 0:
                                    target_cells.append(cell)

                            ## Collect barrel cells that have to be rebuilt
                            else:
                                deta = particle.deta(cell)
                                dphi = particle.dphi(cell)
                                if deta < cell.eta_width/1.7 and dphi < cell.phi_width/1.8:
                                    target_cells.append(cell)

                ## Specify that the particle has deposited its energy
                particle.calo_hit_EM = True
                particle.calo_hit_HAD = True

                ## Modify cell opacity according to particle Pt and dR to center of the cell
                pt = math.log(particle.pt/1000.0 + 1.0)
                for cell in target_cells:
                    dR   = particle.dR(cell)
                    max_opacity = 0.4
                    if self.calo_type == CALO_HAD:
                        max_opacity = 0.2
                    cell.opacity += abs(max_opacity - cell.opacity)*(pt/(pt + 1))*(1/(dR+1))
                    cell.build()
                    self.modified_cells.append(cell)



    ## --------------------------------------- ##
    def reset(self):
        """
        Reset opacity of cells to default value
        """
        
        for cell in self.modified_cells:
            cell.opacity = self.opacity
            cell.build()
        self.modified_cells = []
