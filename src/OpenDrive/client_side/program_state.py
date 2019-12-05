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

#: Requests should only be made when this is True
is_authenticated_at_server = False
#: Not implemented yet.
is_authenticated_at_client = False

#
# APPROACH 1: For every thread functions
#

_is_program_running = threading.Event()
_is_synchronization_running = threading.Event()
_is_watching_running = threading.Event()

inner_thread_events = {}


def add_inner_thread_event(inner_event: threading.Event, global_event: threading.Event, on_clear, on_set):
    """Handles the inner_event when global_event is changed: set, clear
    """
    if global_event not in inner_thread_events:
        inner_thread_events[global_event] = []
    inner_thread_events[global_event].append({"inner_event": inner_event,
                                              "on_clear": on_clear,
                                              "on_set": on_set})


# =============== Program ====================
def program_started() -> None:
    _is_program_running.set()
    for inner_event_dict in inner_thread_events[_is_program_running]:
        inner_event_dict["on_set"](inner_event_dict["inner_event"])


def program_stopped() -> None:
    _is_program_running.clear()
    for inner_event_dict in inner_thread_events[_is_program_running]:
        inner_event_dict["on_clear"](inner_event_dict["inner_event"])


def is_program_running() -> bool:
    return _is_program_running.is_set()


def wait_till_program_is_running(timeout):
    _is_program_running.wait(timeout)


# =============== Synchronization ====================
def synchronization_started() -> None:
    _is_synchronization_running.set()


#
# APPROACH 2: One class: Every thread gets an instance
#
class T:

    _EVENT = 0
    _ON_STARTED = 1
    _ON_STOPPED = 2

    def __init__(self):
        self._event = threading.Event()
        self._sub_events = []

    def started(self):
        self._event.set()
        for event_tup in self._sub_events:
            event_tup[self._ON_STARTED]()

    def stopped(self):
        self._event.clear()
        for event_tup in self._sub_events:
            event_tup[self._ON_STOPPED]()

    def is_running(self):
        return self._event.is_set()

    def wait_till_running(self, timeout=None):
        self._event.wait(timeout)

    def add_sub_event(self, event, on_started, on_stopped):
        self._sub_events.append((event, on_started, on_stopped))


program = T()
gui = T()
synchronization = T()
watching = T()
