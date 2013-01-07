.. #############################################################################
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

.. image:: https://bitbucket.org/emitc2h/cder/raw/5f70f7b0e5362fef614f5abd90f326fc2854306f/core/images/logo.png
   :scale: 25

What is CDER?
-------------

CDER (ColliDER) is a particle physics event visualizer focusing on
high-level objects such as fully reconstructed jets and leptons. The
purpose of CDER is to explore the topology of physics processes. CDER
is designed to be fluid, simple and pretty. It makes extensive use of
the following packages, which must be installed locally

http://root.cern.ch/drupal/

http://www.pyglet.org/

http://code.google.com/p/py-lepton/

CDER itself does not need to be compiled or installed. It should run
out-of-the-box given that the three packages mentioned are installed
and working.

CDER is placed under the GNU General Public Licence

http://www.gnu.org/licenses/


Important
---------

CDER does not yet run in 64 bits. Run in 32-bit mode (python-32). This
is because of the nature of the super-fast random number generators in
py-lepton. This should be fixed at some point in the future.


(Very) quick start
------------------

To launch CDER with the example events::

    python-32 CDER.py

For more information, press 'h' for help and take a look at the wiki

https://bitbucket.org/emitc2h/cder/wiki/Home


Screenshots
-----------

.. image:: https://bitbucket.org/emitc2h/cder/raw/3b60c54c04dcd2734dbe29cd75512c34acd5e3e5/core/images/example.png
