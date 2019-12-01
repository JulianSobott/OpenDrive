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

from OpenDrive.client_side.gui import screens
from OpenDrive.client_side import paths as client_paths
from OpenDrive.client_side import file_changes_json
from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger_general, logger_gui

# DO NOT DELETE UNUSED IMPORTS!
# They are needed inside the OpenDriveApp
from OpenDrive.client_side.gui.authentication import login_manual
from OpenDrive.client_side.gui.authentication import registration
from OpenDrive.client_side.gui.explorer import explorer

app = None


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
         try_auto_login: bool = True, opened_by_server: bool = False):
    global app
    logger_general.info(f"Open GUI by {'Server' if opened_by_server else 'User'}")
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
    main(start_screen=screens.LOGIN_MANUAL, authentication_only=True, try_auto_login=True, opened_by_server=True)


if __name__ == '__main__':
    main()
