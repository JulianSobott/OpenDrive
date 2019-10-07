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


def _open_gui():
    gui.main.main()


def _stop():
    from OpenDrive.client_side.main import shutdown
    shutdown()


def start_tray(background_function):
    """Add an tray icon and is blocking the program. Must be called from the main thread."""
    def background_wrapper(icon_):
        background_function()

    image = PIL.Image.open("assets/Logo.png")
    menu = pystray.Menu(pystray.MenuItem("Open", _open_gui), pystray.MenuItem("Stop", _stop))
    icon = pystray.Icon("OpenDrive", image, "OpenDrive", menu)
    icon.icon = image
    icon.run(background_wrapper)
    icon.visible = True
    logger.info("Tray started")


if __name__ == '__main__':
    def test():
        print("Hello world")
    start_tray(test)
