"""
:module: OpenDrive.client_side.gui.controller
:synopsis: Controlling the opening and closing of the gui
:author: Julian Sobott


public functions
----------------

.. autofunction:: start_gui_thread
.. autofunction:: stop
.. autofunction:: open_gui
.. autofunction:: close_gui

"""
import threading
from kivy.app import App

from OpenDrive.client_side import program_state
from OpenDrive.client_side.gui import main as gui_main
from OpenDrive.client_side.od_logging import logger_gui, init_logging

_open_gui_event = threading.Event()
_app_is_running = False
_open_settings_default = {"authentication_only": False, "opened_by": gui_main.CLIENT}     # TODO: find better solution
_open_settings = _open_settings_default


def start_gui_thread():
    """Starts a thread in which the GUI will run later

    Needs to be called before the GUI is opened.
    This function ensures, that the GUI always runs in the same thread. otherwise there are issues, when the GUI was
    opened and is opened again.
    """
    program_state.gui.started()
    thread = threading.Thread(target=_gui_thread, name="GUI")
    thread.start()


def stop():
    """Closes the GUI and stops the GUI thread.

    WARNING: After this call, the GUI can never be opened again while the program is running.
    """
    close_gui()
    program_state.gui.stopped()


def open_gui(authentication_only=False, opened_by: gui_main.Opener = gui_main.CLIENT):
    """Opens the GUI window."""
    global _app_is_running
    if not _app_is_running:
        logger_gui.info(f"Requests to open GUI: authentication_only={authentication_only}, opened_by={opened_by}")
        _open_gui_event.set()
        _open_settings["authentication_only"] = authentication_only
        _open_settings["opened_by"] = opened_by
        _app_is_running = True
    else:
        logger_gui.info(f"Requests to open GUI but app is already running")


def close_gui():
    """Closes the GUI window."""
    global _app_is_running
    if _app_is_running:
        logger_gui.info(f"Close GUI")
        App.get_running_app().stop()
        _after_close_gui()
    else:
        logger_gui.info(f"Requests to close GUI but app is already closed")


def _after_close_gui():
    global _app_is_running
    _open_gui_event.clear()
    _open_settings.clear()
    _open_settings.update(_open_settings_default)
    _app_is_running = False


def _cleanup_kivy():
    """Resetting the global state of kivy"""
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        for cat in Cache._categories:
            Cache._objects[cat] = {}


def _gui_thread():
    """Every time the GUI shall be opened it is opened here"""
    program_state.gui.add_on_stop(lambda: _open_gui_event.set())    # Wake up when GUI stops
    while program_state.gui.is_running():
        _open_gui_event.wait()      # Wait until the GUI is requested to be opened
        if program_state.gui.is_running():
            _open_gui_from_thread()
            _after_close_gui()
        else:
            pass    # program is closed


def _open_gui_from_thread():
    """Opens the GUI.

    Must be called from the GUI thread.
    """
    logger_gui.info(f"Opening GUI: _open_settings={_open_settings}")
    _cleanup_kivy()
    gui_main.main(**_open_settings)


if __name__ == '__main__':
    init_logging()
    start_gui_thread()
    open_gui()
    import time
    time.sleep(3)
    close_gui()
    program_state.program.stopped()
