"""
===========================================================
Input File
===========================================================
"""

# from reader.lhprocessor_reader import LHProcessor_Reader as reader
# filename = 'LHProcessorCN.VBFH125.root'
# treename = 'lh_train'
# cuts     = ''
# reader(filename, treename, cuts)


"""
===========================================================
Graphics
===========================================================
"""

## ----------------------------------------------------- ##
## Electromagnetic calorimeter

## Display
display_em = True

## Geometry
em_inner_radius  = 1.5
em_outer_radius  = 1.95
em_max_abs_eta   = 1.475
em_eta_divisions = 13
em_phi_divisions = 30
em_endcap_thickness = 0.20


## ----------------------------------------------------- ##
## Hadronic calorimeter

## Display
display_had = True

## Geometry
had_inner_radius  = 2.2
had_outer_radius  = 3.0
had_max_abs_z     = 4.3
had_eta_divisions = 10 
had_phi_divisions = 15 


## ----------------------------------------------------- ##
## Particles
beam_speed = 8.0
particle_speed = 0.05
particle_filling = 1000

