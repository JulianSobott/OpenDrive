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
from pynetworking import client     # Do not delete unused import

sys.path.insert(0, os.path.abspath("../"))
from OpenDrive import client_side


def main():
    client_side.main.start()


if __name__ == '__main__':
    main()
