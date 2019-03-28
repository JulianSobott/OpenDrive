"""
:module: OpenDrive.server_side.paths
:synopsis: All important paths at the server-side
:author: Julian Sobott

public constants
-----------------

"""
import os

paths_PATH = os.path.realpath(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(paths_PATH, "../../../.."))
CODE_PATH = os.path.join(PROJECT_PATH, "src/OpenDrive/")

SERVER_DB_PATH = os.path.join(PROJECT_PATH, "local/server_side/server_data.db")
