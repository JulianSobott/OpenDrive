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
import shutil
import os
from multiprocessing import Process, Queue

import OpenDrive.server_side.net_start
import OpenDrive.client_side.net_start
from OpenDrive import server_side
from OpenDrive import client_side
from OpenDrive.general.database import delete_db_file
from OpenDrive.server_side import paths as server_paths
from OpenDrive.client_side import paths as client_paths

server_stop_queue = Queue()


def delete_recreate_server_db():
    delete_db_file(server_side.paths.SERVER_DB_PATH)
    server_side.database.create_database()


def delete_recreate_client_db():
    delete_db_file(client_side.paths.LOCAL_DB_PATH)
    client_side.database.create_database()


def start_server_process() -> Process:
    server_process = None
    try:
        server_process = Process(target=_debug_server_routine, args=(server_stop_queue,))
        return server_process
    finally:
        server_process.start()


def stop_process(process: Process):
    server_stop_queue.put("Stop")
    process.join()


def client_routine(clear_server_db: bool = False, clear_client_db: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            clear_init_folders()
            if clear_server_db:
                delete_recreate_server_db()
            if clear_client_db:
                delete_recreate_client_db()

            client_net = OpenDrive.client_side.net_start
            connected = client_net.connect(timeout=2)
            if not connected:
                raise ConnectionError
            ret_value = func(*args, **kwargs)
            client_net.close_connection()
            return ret_value
        return wrapper
    return decorator


def h_clear_init_all_folders(client=True, server=True):
    """
    server: OpenDrive/local/server_side/ROOT/
    client: OpenDrive/local/client_side
    """
    if server:
        shutil.rmtree(server_paths.FOLDERS_ROOT, ignore_errors=True)
        os.makedirs(server_paths.FOLDERS_ROOT, exist_ok=True)
    if client:
        shutil.rmtree(client_paths.LOCAL_CLIENT_DATA, ignore_errors=True)
        os.makedirs(client_paths.LOCAL_CLIENT_DATA, exist_ok=True)


def _debug_server_routine(queue: Queue):
    OpenDrive.server_side.net_start.start(queue)

