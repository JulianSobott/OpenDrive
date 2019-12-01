"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
import os
import typing

NormalizedPath = typing.NewType("NormalizedPath", str)

paths_PATH = os.path.realpath(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(paths_PATH, "../../../.."))
CODE_PATH = os.path.join(PROJECT_PATH, "src/OpenDrive/")

LOCAL_DATA = os.path.join(PROJECT_PATH, "local/")
TEMP = os.path.join(PROJECT_PATH, "tmp")
LOGS = os.path.join(TEMP, "logs")
CLIENT_LOGS = os.path.join(LOGS, "client")
SERVER_LOGS = os.path.join(LOGS, "server")


def normalize_path(path: str, *paths: str) -> NormalizedPath:
    full_path = os.path.join(path, *paths)
    normalized_os_path = os.path.normpath(full_path)
    return NormalizedPath(normalized_os_path.replace("\\", "/"))
