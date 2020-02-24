"""
:module: OpenDrive.client_side.program_state
:synopsis: Global program states
:author: Julian Sobott

Thread controlling states
-------------------------

Realized via threading.Event
is_set = True
clear() -> False

- is_program_running
- is_synchronization_running
- is_watching_running

Bool states
-----------

Store global bool states

- is_authenticated_at_server
- is_authenticated_at_local

"""
import threading

__all__ = ["program", "gui", "synchronization", "watching", "is_authenticated_at_server"]


class _ThreadEventHandler:

    def __init__(self):
        self._event = threading.Event()
        self._on_stop = []
        self._on_start = []

    def started(self):
        self._event.set()
        for fun in self._on_start:
            fun()

    def stopped(self):
        self._event.clear()
        for fun in self._on_stop:
            fun()

    def is_running(self):
        return self._event.is_set()

    def wait_till_running(self, timeout=None):
        self._event.wait(timeout)

    def add_on_start(self, function):
        assert function, "Function must be an actual function"
        self._on_start.append(function)

    def add_on_stop(self, function):
        assert function, "Function must be an actual function"
        self._on_stop.append(function)


program = _ThreadEventHandler()
gui = _ThreadEventHandler()
synchronization = _ThreadEventHandler()
watching = _ThreadEventHandler()
is_authenticated_at_server = _ThreadEventHandler()

program.add_on_stop(gui.stopped)
program.add_on_stop(synchronization.stopped)
program.add_on_stop(watching.stopped)

sync_lock = threading.Lock()
