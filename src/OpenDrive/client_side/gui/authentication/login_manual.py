from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger_gui
from OpenDrive.client_side.gui import screens


class ScreenLoginManual(Screen):

    tf_username_email = ObjectProperty(None)
    tf_password = ObjectProperty(None)
    lbl_user_hints = ObjectProperty(None)

    def btn_release_login(self):
        username = self.tf_username_email.text
        password = self.tf_password.text
        status = interface.login_manual(username, password)
        if status.was_successful():
            logger_gui.debug("Successfully logged in")
            screens.screen_manager.do_login()
        else:
            self.lbl_user_hints.color[3] = 1
            self.lbl_user_hints.text = status.get_text()

    def btn_release_register(self):
        screens.screen_manager.set_screen(screens.REGISTRATION)
