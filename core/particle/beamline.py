#**************************************************#
# file   : core/particle/beamline.py               #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Makes a collision animation when switching to a  #
# different event                                  #
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
from pyglet import image
from pyglet.gl import *

## Basic python imports
import os, math, time

## CDER imports
from ..config import *

####################################################
class Beamline():

    ## --------------------------------------- ##
    def __init__(self):
        """
        Constructor
        """

        ## Beams ##
        #---------#
        
        ## Beam parameters
        self.incoming = False
        self.beam_length = beam_speed
        self.beam_start  = beam_speed*12.0 + self.beam_length/2.0
        self.beam_speed  = beam_speed
        
        ## A beam domain
        self.A_beam_position = -self.beam_start

        ## C beam domain
        self.C_beam_position = self.beam_start


    
    ## --------------------------------------- ##
    def update(self, dt):
        """
        Behaviour of the beams in time
        """

        ## Check that beams haven't reached collision point
        ## Both beams should be perfectly sychronized, check beam A only
        if self.A_beam_position <= -self.beam_length/2:

            ## Update A beam position
            self.A_beam_position += self.beam_speed

            ## Update C beam position
            self.C_beam_position -= self.beam_speed

        ## When beams reach the collision point, make the collision animation
        else:
            if self.incoming:
                self.collide(0)          

            ## Make the beams disappear, the beams are not in motion anymore
            self.stop()


    
    ## --------------------------------------- ##
    def start(self):
        """
        Start the collision animation
        """

        ## The beam is in motion
        self.incoming = True

        

    ## --------------------------------------- ##
    def A_stop(self):
        """
        Stop A beam
        """


            
    ## --------------------------------------- ##
    def C_stop(self):
        """
        Stop C beam
        """

            
    ## --------------------------------------- ##
    def stop(self):
        """
        Stop both A and C beam, beams not in motion
        """
        
        if self.incoming:
            self.A_stop()
            self.C_stop()
            self.incoming = False


            
    ## --------------------------------------- ##
    def collide(self,dt):
        """
        Make the collision animation
        """
        