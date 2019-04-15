"""
:module: OpenDrive.server_side.paths
:synopsis: All important paths at the server-side
:author: Julian Sobott

public constants
-----------------

"""
import os

from OpenDrive.general.paths import *


LOCAL_SERVER_DATA = os.path.join(LOCAL_DATA, "server_side/")

SERVER_DB_PATH = os.path.join(LOCAL_SERVER_DATA, "server_data.db")

FOLDERS_ROOT = os.path.join(LOCAL_SERVER_DATA, "ROOT/")
