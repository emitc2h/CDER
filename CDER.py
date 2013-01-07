#**************************************************#
# file   : CDER.py                                 #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Main script to launch CDER                       #
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

import pyglet
from core import config

####################################################
## Instantiate calorimeter and beamline
calorimeters = []
if config.em_display  :
    from core.calorimeter import em
    calorimeters.append(em.EM_Calorimeter())
if config.had_display :
    from core.calorimeter import had
    calorimeters.append(had.HAD_Calorimeter())
    
from core.particle import beamline
beam = beamline.Beamline()


####################################################
## Instantiate Display
from core.display import Display
display = Display(calorimeters, beam)
display.clear()

        
####################################################
## Run pyglet:
if __name__ == '__main__':
    pyglet.app.run()
