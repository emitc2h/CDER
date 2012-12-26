#**************************************************#
# file   : core/config.py                          #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# Load config.ini into python objects to be handed #
# to the rest of the code                          #
#**************************************************#

import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read('config.ini')

"""
===========================================================
Input File
===========================================================
"""

filename   = conf.get('InputFile', 'filename')
treename   = conf.get('InputFile', 'treename')
filereader = conf.get('InputFile', 'filereader')


"""
===========================================================
Graphics
===========================================================
"""

## ----------------------------------------------------- ##
## Electromagnetic calorimeter

## Display
em_display = conf.getboolean('Graphics', 'em_display')

## Geometry
em_inner_radius  = conf.getfloat('Graphics', 'em_inner_radius')
em_outer_radius  = conf.getfloat('Graphics', 'em_outer_radius')
em_max_abs_eta   = conf.getfloat('Graphics', 'em_max_abs_eta')
em_eta_divisions = conf.getint('Graphics', 'em_eta_divisions')
em_phi_divisions = conf.getint('Graphics', 'em_phi_divisions')
em_endcap_thickness = conf.getfloat('Graphics', 'em_endcap_thickness')


## ----------------------------------------------------- ##
## Hadronic calorimeter

## Display
had_display = conf.getboolean('Graphics', 'had_display')

## Geometry
had_inner_radius  = conf.getfloat('Graphics', 'had_inner_radius')
had_outer_radius  = conf.getfloat('Graphics', 'had_outer_radius')
had_max_abs_z     = conf.getfloat('Graphics', 'had_max_abs_z')
had_eta_divisions = conf.getint('Graphics', 'had_eta_divisions')
had_phi_divisions = conf.getint('Graphics', 'had_phi_divisions')


## ----------------------------------------------------- ##
## Particles
beam_speed       = conf.getfloat('Graphics', 'beam_speed')
particle_speed   = conf.getfloat('Graphics', 'particle_speed')
particle_filling = conf.getint('Graphics', 'particle_filling')


"""
===========================================================
Camera control
===========================================================
"""

## Pitch and yaw control
yaw_speed   = conf.getfloat('Camera', 'yaw_speed')
pitch_speed = conf.getfloat('Camera', 'pitch_speed')
min_pitch   = conf.getfloat('Camera', 'min_pitch')
max_pitch   = conf.getfloat('Camera', 'max_pitch')

## Zoom control
zoom_speed  = conf.getfloat('Camera', 'zoom_speed')
min_zoom    = conf.getfloat('Camera', 'min_zoom')
max_zoom    = conf.getfloat('Camera', 'max_zoom')
