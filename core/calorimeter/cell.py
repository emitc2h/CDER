#**************************************************#
# file   : core/calorimeter/cell.py                #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A single calorimeter cell.                       #
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
from pyglet.gl import *

## Basic python imports
import math

## CDER imports
from ..utils import *

## Default strings for geometry types
GEO_PROJECTIVE  = 'projective'
GEO_CYLINDRICAL = 'cylindrical'

####################################################
class Cell():

    ## --------------------------------------- ##
    def __init__(self, parameters, geometry, inner_color, outer_color, opacity=0.3):
        """
        Constructor
        """

        ## Check that a 6-tuple is provided
        n_parameters = len(parameters)
        if n_parameters != 6:
            raise ValueError('There should be 6 parameters to define the cell. Only %d provided.' % n_parameters)

        ## Specify cell geometry
        self.geometry = geometry

        ## Set projective geometry parameters
        if self.geometry == GEO_PROJECTIVE:
            self.inner_radius = parameters[0]
            self.outer_radius = parameters[1]
            self.eta_center   = parameters[2]
            self.eta_width    = parameters[3]
            self.phi_center   = parameters[4]
            self.phi_width    = parameters[5]

            ## Calculate positions of the cell corners in cartesian coordinates and
            ## calculate corresponding cylindrical parameters
            self.calculate_coordinates_projective()

        ## Set cylindrical geometry parameters
        elif self.geometry == GEO_CYLINDRICAL:
            self.inner_radius = parameters[0]
            self.outer_radius = parameters[1]
            self.z_center     = parameters[2]
            self.z_width      = parameters[3]
            self.phi_center   = parameters[4]
            self.phi_width    = parameters[5]

            ## Calculate positions of the cell corners in cartesian coordinates and
            ## Calculate corresponding projective parameters
            self.calculate_coordinates_cylindrical()

        ## Color gradient from inside to outside
        self.outer_color = outer_color
        self.inner_color = inner_color

        ## Cell opacity (also serves to display cell energy)
        self.opacity = opacity

        ## radial distance For initial calorimeter construction animation
        self.distance = 0.0

        ## Compiled list of openGL objects
        self.display_list = None

        ## Compile the calorimeter cell
        self.build()


        
    ## --------------------------------------- ##
    def calculate_coordinates_projective(self):
        """
        Calculate the catersian coordinates of the cell corners in the case of projective geometry and 
        the values of associated cylindrical geometry parameters
        """

        ## Calculate the coordinates of the 8 corners
        raw_outer_1 = (self.outer_radius, self.eta_center-self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_2 = (self.outer_radius, self.eta_center+self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_3 = (self.outer_radius, self.eta_center+self.eta_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_outer_4 = (self.outer_radius, self.eta_center-self.eta_width/2.0, self.phi_center+self.phi_width/2.0)

        raw_inner_1 = (self.inner_radius, self.eta_center-self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_2 = (self.inner_radius, self.eta_center+self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_3 = (self.inner_radius, self.eta_center+self.eta_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_inner_4 = (self.inner_radius, self.eta_center-self.eta_width/2.0, self.phi_center+self.phi_width/2.0)

        ## Convert to cartesian coordinates
        self.outer_1 = rap_to_cart(raw_outer_1)
        self.outer_2 = rap_to_cart(raw_outer_2)
        self.outer_3 = rap_to_cart(raw_outer_3)
        self.outer_4 = rap_to_cart(raw_outer_4)

        self.inner_1 = rap_to_cart(raw_inner_1)
        self.inner_2 = rap_to_cart(raw_inner_2)
        self.inner_3 = rap_to_cart(raw_inner_3)
        self.inner_4 = rap_to_cart(raw_inner_4)

        ## Calculate position and width in z
        self.z_center = eta_to_z(((self.inner_radius+self.outer_radius)/2, self.eta_center))

        z_lo = eta_to_z(((self.inner_radius+self.outer_radius)/2, self.eta_center - self.eta_width))
        z_hi = eta_to_z(((self.inner_radius+self.outer_radius)/2, self.eta_center + self.eta_width))

        self.z_width = abs(z_lo - z_hi)



    ## --------------------------------------- ##
    def calculate_coordinates_cylindrical(self):
        """
        Calculate the catersian coordinates of the cell corners in the case of cylindrical geometry and 
        the values of associated projective geometry parameters
        """

        ## Calculate the coordinates of the 8 corners
        raw_outer_1 = (self.outer_radius, self.z_center-self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_2 = (self.outer_radius, self.z_center+self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_3 = (self.outer_radius, self.z_center+self.z_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_outer_4 = (self.outer_radius, self.z_center-self.z_width/2.0, self.phi_center+self.phi_width/2.0)

        raw_inner_1 = (self.inner_radius, self.z_center-self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_2 = (self.inner_radius, self.z_center+self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_3 = (self.inner_radius, self.z_center+self.z_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_inner_4 = (self.inner_radius, self.z_center-self.z_width/2.0, self.phi_center+self.phi_width/2.0)

         ## Convert to cartesian coordinates
        self.outer_1 = cyl_to_cart(raw_outer_1)
        self.outer_2 = cyl_to_cart(raw_outer_2)
        self.outer_3 = cyl_to_cart(raw_outer_3)
        self.outer_4 = cyl_to_cart(raw_outer_4)

        self.inner_1 = cyl_to_cart(raw_inner_1)
        self.inner_2 = cyl_to_cart(raw_inner_2)
        self.inner_3 = cyl_to_cart(raw_inner_3)
        self.inner_4 = cyl_to_cart(raw_inner_4)

        ## Calculate position and width in eta
        self.eta_center = z_to_eta(((self.inner_radius+self.outer_radius)/2, self.z_center))

        eta_lo = z_to_eta(((self.inner_radius+self.outer_radius)/2, self.z_center - self.z_width))
        eta_hi = z_to_eta(((self.inner_radius+self.outer_radius)/2, self.z_center + self.z_width))

        self.eta_width = abs(eta_lo - eta_hi)



    ## --------------------------------------- ##
    def build(self):
        """
        Make the list of OpenGL quads from the corner cartesian coordinates and
        compile
        """

        ## Instantiate openGL list to be compiled
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        glBegin(GL_QUADS)

        ## Top
        glColor4f( self.outer_color[0], self.outer_color[1], self.outer_color[2], self.opacity )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )

        ## Bottom
        glColor4f( self.inner_color[0], self.inner_color[1], self.inner_color[2], self.opacity )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )

        ## Front
        glColor4f( self.outer_color[0], self.outer_color[1], self.outer_color[2], self.opacity )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glColor4f( self.inner_color[0], self.inner_color[1], self.inner_color[2], self.opacity )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )

        ## Back
        glColor4f( self.outer_color[0], self.outer_color[1], self.outer_color[2], self.opacity )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glColor4f( self.inner_color[0], self.inner_color[1], self.inner_color[2], self.opacity )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )

        ## Left
        glColor4f( self.outer_color[0], self.outer_color[1], self.outer_color[2], self.opacity )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )
        glColor4f( self.inner_color[0], self.inner_color[1], self.inner_color[2], self.opacity )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )

        ## Right
        glColor4f( self.outer_color[0], self.outer_color[1], self.outer_color[2], self.opacity )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glColor4f( self.inner_color[0], self.inner_color[1], self.inner_color[2], self.opacity )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )

        glEnd()

        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex3f( 0, 0, 0 )
        glColor4f( 0, 0, 0, 0.0 )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glEnd()

        glEndList()

        

    ## --------------------------------------- ##
    def draw(self):
        """
        Draw the cell at the distance set
        """

        ## Add distance from the z-axis
        move_x = self.distance*math.cos(self.phi_center)
        move_y = self.distance*math.sin(self.phi_center)
        
        glTranslatef(move_x, move_y, 0.0)
        glCallList(self.display_list)
        glTranslatef(-move_x, -move_y, 0.0)



        
