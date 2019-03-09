"""
@author: Julian Sobott
@brief: All paths, that are important at the client_side
@description:

@external_use:

@internal_use:
"""
import os

paths_PATH = os.path.realpath(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(paths_PATH, "../../../.."))
CODE_PATH = os.path.join(PROJECT_PATH, "src/OpenDrive/")

LOCAL_DB_PATH = os.path.join(PROJECT_PATH, "local/client_Side/local_data.db")
