"""
:module: OpenDrive.start_client
:synopsis: Entry point for the client
:author: Julian Sobott

public functions
----------------

.. autofunction:: main

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
