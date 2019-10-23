"""
:module: OpenDrive.
:synopsis: 
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
import sys
import os

sys.path.insert(0, os.path.abspath("../"))
from OpenDrive.client_side import main

main.start()
