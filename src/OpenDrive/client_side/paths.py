"""
:module: OpenDrive.client_side.paths
:synopsis: All relevant paths for the client
:author: Julian Sobott

public module members
----------------------

.. autodata:: LOCAL_CLIENT_DATA
.. autodata:: LOCAL_DB_PATH
.. autodata:: LOCAL_JSON_PATH
.. autodata:: AUTHENTICATION_PATH

"""
from OpenDrive.general.paths import *

LOCAL_CLIENT_DATA = normalize_path(LOCAL_DATA, "client_side")

LOCAL_DB_PATH = normalize_path(LOCAL_CLIENT_DATA, "local_data.db")
LOCAL_JSON_PATH = normalize_path(LOCAL_CLIENT_DATA, "changes.json")
AUTHENTICATION_PATH = normalize_path(LOCAL_CLIENT_DATA, "authentication.txt")

ASSETS = normalize_path(CODE_PATH, "client_side/gui/assets")
