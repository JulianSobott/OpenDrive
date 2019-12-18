"""
:module: OpenDrive.
:synopsis: 
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
from OpenDrive.client_side import paths as c_paths


def get_image_path(image: str) -> str:
    return c_paths.normalize_path(c_paths.ASSETS, image)
