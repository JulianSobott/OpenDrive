"""
:module: 
:synopsis: Module provide functions for easier testing communication.
:author: Julian Sobott


public classes
---------------

.. autoclass:: XXX
    :members:
    
public functions
-----------------

.. autofunction:: XXX

private classes
----------------

private functions
------------------

"""
from multiprocessing import Process

import OpenDrive.server_side.net_start
import OpenDrive.client_side.net_start
from OpenDrive import server_side
from OpenDrive import client_side
from OpenDrive.general.database import delete_db_file


def delete_recreate_server_db():
    delete_db_file(server_side.paths.SERVER_DB_PATH)
    server_side.database.create_database()


def delete_recreate_client_db():
    delete_db_file(client_side.paths.LOCAL_DB_PATH)
    client_side.database.create_database()


def start_server_process() -> Process:
    server_process = None
    try:
        server_process = Process(target=_debug_server_routine)
        return server_process
    finally:
        server_process.start()


def stop_process(process: Process):
    process.kill()


def client_routine(clear_server_db: bool = False, clear_client_db: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if clear_server_db:
                delete_recreate_server_db()
            if clear_client_db:
                delete_recreate_client_db()

            client_net = OpenDrive.client_side.net_start
            client_net.connect()
            ret_value = func(*args, **kwargs)
            client_net.close_connection()
            return ret_value
        return wrapper
    return decorator


def _debug_server_routine():
    OpenDrive.server_side.net_start.start()

