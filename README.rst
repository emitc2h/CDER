.. image:: https://bitbucket.org/emitc2h/cder/raw/5f70f7b0e5362fef614f5abd90f326fc2854306f/core/images/logo.png
   :scale: 25

What is CDER?
-------------

CDER (ColliDER) is a particle physics event visualizer focusing on
high-level objects such as fully reconstructed jets and leptons. The
purpose of CDER is to explore the topology of physics processes. CDER
is designed to be fluid, simple and pretty. It makes extensive use of
the following packages, which must be installed locally

_http://root.cern.ch/drupal/
_http://www.pyglet.org/
_http://code.google.com/p/py-lepton/

.. _http://root.cern.ch/drupal/: http://root.cern.ch/drupal/
.. _http://www.pyglet.org/: http://www.pyglet.org/
.. _http://code.google.com/p/py-lepton/: http://code.google.com/p/py-lepton/

CDER itself does not need to be compiled or installed. It should run
out-of-the-box given that the three packages mentioned are installed
and working.


Important
---------

CDER does not yet run in 64 bits. Run in 32-bit mode (python-32). This
is because of the nature of the super-fast random number generators in
py-lepton. This should be fixed at some point in the future.


(Very) quick start
------------------

To launch CDER with the example events::

    python-32 CDER.py

For more information, press 'h' for help and take a look at the wiki:

_https://bitbucket.org/emitc2h/cder/wiki/Home

.. _https://bitbucket.org/emitc2h/cder/wiki/Home: https://bitbucket.org/emitc2h/cder/wiki/Home


Screenshots
-----------

.. image:: https://bitbucket.org/emitc2h/cder/raw/5f70f7b0e5362fef614f5abd90f326fc2854306f/core/images/example.png
