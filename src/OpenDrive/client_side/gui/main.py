"""
:module: OpenDrive.client_side.gui.main
:synopsis: Main gui window
:author: Julian Sobott

public classes
---------------

.. autoclass:: TestApp
    :members:
    
public functions
-----------------

.. autofunction:: XXX

private classes
----------------

private functions
------------------

"""
import os
from kivy.app import App

from OpenDrive.client_side.gui import screens
from OpenDrive.client_side import paths as client_paths

# DO NOT DELETE UNUSED IMPORTS!
# They are needed inside the OpenDriveApp
from OpenDrive.client_side.gui.authentication import login_manual
from OpenDrive.client_side.gui.authentication import registration
from OpenDrive.client_side.gui.explorer import explorer


class OpenDriveApp(App):
    pass


def main():
    os.chdir(os.path.join(client_paths.CODE_PATH, "client_side/gui/"))
    app.run()


app = OpenDriveApp()
screens.screen_manager = screens.ScreenManager(app)


def open_authentication_window():
    """Opens a window where the user can log in. After successful login the window is closed"""
    main()


if __name__ == '__main__':
    main()
