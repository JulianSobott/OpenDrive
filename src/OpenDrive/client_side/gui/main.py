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
from OpenDrive.client_side import file_changes_json

# DO NOT DELETE UNUSED IMPORTS!
# They are needed inside the OpenDriveApp
from OpenDrive.client_side.gui.authentication import login_manual
from OpenDrive.client_side.gui.authentication import registration
from OpenDrive.client_side.gui.explorer import explorer


class OpenDriveApp(App):

    def __init__(self, start_screen: screens.ScreenName = screens.LOGIN_MANUAL, authentication_only: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.start_screen = start_screen
        self.authentication_only = authentication_only

    def build(self):
        screens.screen_manager.set_screen(self.start_screen)


def main(start_screen: screens.ScreenName = screens.LOGIN_MANUAL, authentication_only: bool = False):
    file_changes_json.init_file()
    app = OpenDriveApp(start_screen, authentication_only)
    screens.screen_manager = screens.ScreenManager(app)
    os.chdir(os.path.join(client_paths.CODE_PATH, "client_side/gui/"))
    app.run()


def open_authentication_window():
    """Opens a window where the user can log in. After successful login the window is closed"""
    main(start_screen=screens.LOGIN_MANUAL, authentication_only=True)


if __name__ == '__main__':
    main()
