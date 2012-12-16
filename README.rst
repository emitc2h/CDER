What is this?
-------------

A high-level event visualiser interfacing ROOT ntuples
of a pre-determined format to an OpenGL graphics display.
This package depends on ROOT, pyglet, py-lepton and PyOpenGL::

    http://root.cern.ch/drupal/
    http://www.pyglet.org/
    http://code.google.com/p/py-lepton/
    http://pyopengl.sourceforge.net/

The code is not strongly dependent on versions, but I'll try
to recommend specific versions in the future here.


Important
--------

The package does not run in 64-bits. Run in 32-bit mode
(python-32). This is because of the nature of the super-fast random
number generators in py-lepton, and the treatment of OpenGL graphics
by pyglet.
