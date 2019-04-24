"""
@author: Julian Sobott
@brief:
@description:

@external_use:

@internal_use:
"""
from OpenDrive.server_side import paths
from OpenDrive.server_side import database
from OpenDrive.server_side import net_start
from OpenDrive.server_side import folders


def h_execute_function(func, *args, **kwargs):
    """Helper to simulate client calls, to specific functions"""
    func(*args, **kwargs)


def h_dummy():
    return 10