"""
:module: OpenDrive.start_server
:synopsis: Entry point for the server
:author: Julian Sobott
"""
import sys
import os
from pynetworking import server

sys.path.insert(0, os.path.abspath("../"))
from OpenDrive.server_side import net_start


if __name__ == '__main__':
    net_start.start()
