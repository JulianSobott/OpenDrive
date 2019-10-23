"""
:module: OpenDrive.client_side.tray
:synopsis: Tray Icon for opening the gui
:author: Julian Sobott

public functions
----------------

.. autofunction:: start_tray()

private functions
-----------------

.. autofunction:: _open_gui()

.. autofunction:: _stop()



"""
import pystray
import PIL.Image

from OpenDrive.client_side import gui
from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side import paths as c_paths

tray = None


def _open_gui():
    gui.main.main()


def start_tray(background_function, shutdown_function):
    """Add an tray icon and is blocking the program. Must be called from the main thread."""
    global tray

    def background_wrapper(icon_):
        background_function()

    def _stop():
        """
        Stops synchronization. Tray keeps open
        """
        shutdown_function()

    def _close():
        """
        Stops synchronization and stops the tray.
        """
        shutdown_function()
        stop_tray()

    image = PIL.Image.open(c_paths.normalize_path(c_paths.ASSETS, "Logo.png"))
    menu = pystray.Menu(pystray.MenuItem("Open", _open_gui), pystray.MenuItem("Stop", _stop),
                        pystray.MenuItem("Close", _close))
    tray = pystray.Icon("OpenDrive", image, "OpenDrive", menu)
    tray.icon = image
    tray.visible = True
    logger.info("Tray started")
    tray.run(background_wrapper)


def stop_tray():
    global tray
    tray.stop()


if __name__ == '__main__':
    def test():
        print("Hello world")
    start_tray(test, test)
