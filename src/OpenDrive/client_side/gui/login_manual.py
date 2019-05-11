from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side.gui import screens


class ScreenLoginManual(Screen):

    tf_username = ObjectProperty(None)
    tf_password = ObjectProperty(None)

    def btn_release_login(self):
        username = self.tf_username.text
        password = self.tf_password.text
        status = interface.login_manual(username, password)
        if status.was_successful():
            logger.debug("Successfully logged in")
            screens.screen_manager.set_screen(screens.EXPLORER)
        else:
            logger.debug("Login failed TODO")
            logger.debug(status.get_text())
