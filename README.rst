.. image:: https://bitbucket.org/emitc2h/collider/raw/4ae7adec5db93d7e99c9a8fe8064eb223a0035e2/core/images/logo.png

What is this?
-------------

CDER (ColliDER) is a high-level event visualiser interfacing ROOT ntuples
of a pre-determined format to an OpenGL graphics display.
This package depends on ROOT, pyglet, py-lepton and PyOpenGL::

    http://root.cern.ch/drupal/
    http://www.pyglet.org/
    http://code.google.com/p/py-lepton/
    http://pyopengl.sourceforge.net/

The code is not strongly dependent on versions, but I'll try
to recommend specific versions in the future here.

On the other hand, all packages should be compiled in
32-bits. py-lepton is not working very well in 64-bits, so ROOT must
be compiled in 32-bits as well for Collider to work. I hope this will
be resolved in the future.


Important
---------

The package does not run in 64-bits. Run in 32-bit mode
(python-32). This is because of the nature of the super-fast random
number generators in py-lepton, and the treatment of OpenGL graphics
by pyglet.

How does it work?
-----------------

Simply specify an input file by setting in core/config.py::

    filename = 'YourROOTfile.root'
    treename = 'TheTreeInYourROOTfile'

and then launch collider::

    python-32 Collider.py

Pressing the right(left) arrow key lets you navigate to the
next(previous) event in the tree. Pressing the up/down key gives you a
randomly selected event.

Click and drag to rotate around the scene, wheel up/down to zoom
in/out.

You can adjust the complexity of the calorimeter (and take it away
altogether) by changing the parameters in config.py. This may be
useful if the refresh rate is not fast enough.


What does it look like?
-----------------------

.. image:: https://bitbucket.org/emitc2h/collider/raw/dd107417f5162fe84aef35c9b36e3b824c0834e6/example.png
