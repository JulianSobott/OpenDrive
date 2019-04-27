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


def normalize_path(path: str) -> str:
    normalized_os_path = os.path.normpath(path)
    return normalized_os_path.replace("\\", "/")

