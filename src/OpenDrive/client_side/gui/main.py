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
import threading
from typing import NewType

from OpenDrive.client_side.gui import screens
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger_general, logger_gui
from OpenDrive.client_side import program_state

# DO NOT DELETE UNUSED IMPORTS!
# They are needed inside the OpenDriveApp
from OpenDrive.client_side.gui.authentication import login_manual
from OpenDrive.client_side.gui.authentication import registration
from OpenDrive.client_side.gui.explorer import explorer

app = None

Opener = NewType("Opener", str)
SERVER = Opener("server")
CLIENT = Opener("client")
USER = Opener("user")


class OpenDriveApp(App):

    def __init__(self, start_screen: screens.ScreenName, authentication_only: bool, try_auto_login: bool, **kwargs):
        super().__init__(**kwargs)
        logger_gui.info(f"Open app: start_screen={start_screen}, authentication_only={authentication_only}, "
                        f"try_auto_login={try_auto_login}")
        self.start_screen = start_screen
        self.authentication_only = authentication_only
        self.close_on_run = False
        if try_auto_login:
            status = interface.login_auto()
            if status.was_successful():
                if authentication_only:
                    self.close_on_run = True
                else:
                    self.start_screen = screens.EXPLORER

    def build(self):
        screens.screen_manager.set_screen(self.start_screen)

    def run(self):
        if self.close_on_run:
            self.stop()
        else:
            super().run()


def main(start_screen: screens.ScreenName = screens.LOGIN_MANUAL, authentication_only: bool = False,
         try_auto_login: bool = True, opened_by: Opener = CLIENT):
    global app
    # TODO: do not open gui, when auto_login succeeds. Maybe create new authenticate function
    if program_state.is_authenticated_at_server:
        if authentication_only:
            return
        else:
            start_screen = screens.EXPLORER
            try_auto_login = False
    else:
        pass
    logger_general.info(f"Open GUI by {opened_by}")
    file_changes_json.init_file()       # TODO: Needed?
    app = OpenDriveApp(start_screen, authentication_only, try_auto_login)
    screens.screen_manager = screens.ScreenManager(app)
    os.chdir(os.path.join(client_paths.CODE_PATH, "client_side/gui/"))
    threading.Thread(target=app.run).start()


def stop():
    global app
    if app:
        app.stop()
        logger_general.info("Stopped GUI")


def open_authentication_window():
    """Opens a window where the user can log in. After successful login the window is closed"""
    main(start_screen=screens.LOGIN_MANUAL, authentication_only=True, try_auto_login=True, opened_by=SERVER)


if __name__ == '__main__':
    main()
