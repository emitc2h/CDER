#**************************************************#
# file   : CDER.py                                 #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Main script to launch CDER                       #
#**************************************************#

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
