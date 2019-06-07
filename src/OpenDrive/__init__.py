"""
:module: OpenDrive
:synopsis: All source code files for the program
:author: Julian Sobott

The code is mainly split into 3 packages. Code in the client_side and server_side run only on the one side. Both
packages don't are fully independent from each other. Both packages use the general package.

The only file that is located directly in this package is the `net_interface` module. This module defines all
necessary stuff for the `pynetworking` library.

"""

from OpenDrive import client_side
from OpenDrive import server_side
from OpenDrive import general
from OpenDrive import net_interface
