"""
@author: Julian Sobott
@brief: All paths, that are important at the client_side
@description:

@external_use:

@internal_use:
"""
import os

from OpenDrive.general.paths import *

LOCAL_CLIENT_DATA = os.path.join(LOCAL_DATA, "client_side")

LOCAL_DB_PATH = os.path.join(LOCAL_CLIENT_DATA, "local_data.db")
LOCAL_JSON_PATH = os.path.join(LOCAL_CLIENT_DATA, "changes.json")
AUTHENTICATION_PATH = os.path.join(LOCAL_CLIENT_DATA, "authentication.txt")
