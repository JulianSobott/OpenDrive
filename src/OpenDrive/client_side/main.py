"""
:module: OpenDrive.client_side.main
:synopsis: Main script, that defines the execution order.
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
from OpenDrive.client_side import file_changes as c_file_changes


def start():
    """Function that setups everything."""
    c_file_changes.start_observing()

