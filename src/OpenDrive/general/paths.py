"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
import os


def normalize_path(path: str) -> str:
    normalized_os_path = os.path.normpath(path)
    return normalized_os_path.replace("\\", "/")

