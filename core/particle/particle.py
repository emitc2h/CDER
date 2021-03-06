#**************************************************#
# file   : core/particle/particle.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A single particle making up the objects to be    #
# displayed. Also provides information to interact #
# with the calorimeters                            #
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
import os, math, time

## CDER imports
from ..utils import *
from ..config import *

####################################################
class Particle():

    ## --------------------------------------- ##
    def __init__(self, pt, eta, phi, color, isEM=True, isHAD=True, is_min_ion=False, wide=False):
        """
        Constructor
        """

        ## Particle characteristics ##
        #----------------------------#

        ## Basic kinematics
        self.pt  = pt
        self.eta = eta
        self.phi = phi

        ## Particle Color
        self.color = color

        ## Does the particle interact with EM and/or HAD calorimeters?
        self.isEM  = isEM
        self.isHAD = isHAD

        ## Other prooerties
        self.is_min_ion = is_min_ion
        self.wide       = wide

        ## Time sensitive indicators for particle travel animation and
        ## calorimeter animation
        self.calo_hit_EM = True
        self.calo_hit_HAD = True

        ## Does the particle pass through the calorimeters?
        self.is_min_ion = is_min_ion

        self.display_list = None

        self.build()


            
    ## --------------------------------------- ##
    def dR(self, cell):
        """
        Calculates dR w.r.t. a calorimeter cell
        """
        
        return math.sqrt((self.eta - cell.eta_center)**2 + delta_phi(self.phi, cell.phi_center)**2)


    
    ## --------------------------------------- ##
    def deta(self, cell):
        """
        Calculates delta eta w.r.t. a calorimeter cell
        """
        
        return abs(self.eta - cell.eta_center)


    
    ## --------------------------------------- ##
    def dphi(self, cell):
        """
        Calculates delta phi w.r.t. a calorimeter cell
        """
        
        return delta_phi(self.phi, cell.phi_center)



    ## --------------------------------------- ##
    def build(self):
        """
        Make the OpenGL line from the corner cartesian coordinates and
        compile
        """

        ## Particle domain geometry ##
        #----------------------------#
        
        ## If the particle is minimum-ionizing, make it cross the calorimeter
        if self.is_min_ion:
            self.r = 3*em_inner_radius
            ## Change the endcap boundary
            em_inner_z = 3*(1.0 - em_endcap_thickness/2)*eta_to_z((em_outer_radius, em_max_abs_eta))

        ## If the particle is not mimimum-ionizing, set the boundaries to the interior of the
        ## EM calorimeter
        else:
            self.r = em_inner_radius
            em_inner_z = (1.0 - em_endcap_thickness/2)*eta_to_z((em_outer_radius, em_max_abs_eta))

        ## Calculate the cartesian coordinate of the particle to know 
        ## if it ends up in the barrel or in the endcap
        cartesian_endpoint = rap_to_cart((em_inner_radius, self.eta, self.phi))

        ## Check that z is above em endcap
        self.in_endcap = False

        ## width
        width = 3
        if self.wide:
            width = 15
            
        ## Identify if the particle ends up in the barrel region,
        ## Change the endpoint radial distance accordingly
        if abs(cartesian_endpoint[2]) >= em_inner_z:
            self.in_endcap = True
            self.r = (em_inner_z/abs(cartesian_endpoint[2]))*em_inner_radius

        ## Calculate the new cartesian endpoint
        self.cartesian_endpoint = rap_to_cart((self.r, self.eta, self.phi))

        ## Instantiate openGL list to be compiled
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)

        glLineWidth(width)

        glBegin(GL_LINES)
        glColor4f( self.color[0], self.color[1], self.color[2], 1.0)
        glVertex3f( 0.0, 0.0, 0.0 )
        glColor4f( self.color[0], self.color[1], self.color[2], 0.8)
        glVertex3f( self.cartesian_endpoint[0], self.cartesian_endpoint[1], self.cartesian_endpoint[2] )
        glEnd()

        if self.wide:
            glLineWidth(width-3)

            glBegin(GL_LINES)
            glColor4f( self.color[0], self.color[1], self.color[2], 1.0)
            glVertex3f( 0.0, 0.0, 0.0 )
            glColor4f( self.color[0], self.color[1], self.color[2], 0.8)
            glVertex3f( self.cartesian_endpoint[0], self.cartesian_endpoint[1], self.cartesian_endpoint[2] )
            glEnd()

            glLineWidth(width-6)

            glBegin(GL_LINES)
            glColor4f( self.color[0], self.color[1], self.color[2], 1.0)
            glVertex3f( 0.0, 0.0, 0.0 )
            glColor4f( self.color[0], self.color[1], self.color[2], 0.8)
            glVertex3f( self.cartesian_endpoint[0], self.cartesian_endpoint[1], self.cartesian_endpoint[2] )
            glEnd()

            glLineWidth(width-9)

            glBegin(GL_LINES)
            glColor4f( self.color[0], self.color[1], self.color[2], 1.0)
            glVertex3f( 0.0, 0.0, 0.0 )
            glColor4f( self.color[0], self.color[1], self.color[2], 0.8)
            glVertex3f( self.cartesian_endpoint[0], self.cartesian_endpoint[1], self.cartesian_endpoint[2] )
            glEnd()


        glEndList()




    ## --------------------------------------- ##
    def draw(self):
        """
        draws the particle
        """

        glCallList(self.display_list)




    ## --------------------------------------- ##
    def delete(self):
        """
        Clear the display list from OpenGL
        """

        glDeleteLists(self.display_list, 1)
