from kivy.uix.button import Button

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side.gui import screens


class BtnLogin(Button):

    def on_release(self):
        username = ""
        password = ""
        status = interface.login_manual(username, password)
        if status.was_successful() or True:
            logger.debug("Successfully logged in")
            screens.screen_manager.set_screen(screens.EXPLORER)
        else:
            logger.debug("Login failed TODO")
            logger.debug(status.get_text())

