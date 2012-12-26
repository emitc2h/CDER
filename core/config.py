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

