"""
:module: OpenDrive.general.device_data
:synopsis: Functions for getting special device data
:author: Julian Sobott
    
public functions
-----------------

.. autofunction:: get_mac


"""
import uuid


def get_mac() -> str:
    """:returns the devices mac address in the following format: '31028682264019'"""
    return str(uuid.getnode())
