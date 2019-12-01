"""
:module: OpenDrive.client_Side
:synopsis: All source code that is only necessary at the clients device.
:author: Julian Sobott

In this package, the code for the backend is located. The backend handles mainly the synchronization, tracking of
changes and authentication. The GUI stuff is located in a more inner package.

"""
from OpenDrive.client_side import paths
from OpenDrive.client_side import authentication
from OpenDrive.client_side import net_start
from OpenDrive.client_side import interface
from OpenDrive.client_side import file_changes
from OpenDrive.client_side import main
