"""
:module: OpenDrive.client_side.program_state
:synopsis: Global program states
:author: Julian Sobott

"""

#: Requests should only be made when this is True
import threading

is_authenticated_at_server = False

program_is_running = threading.Event()
program_is_running.set()
# TODO: Add nice API
# TODO: Add list of signals that are waiting for something. Set them when program is closed

