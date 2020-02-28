import re

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from OpenDrive.client_side import interface
from OpenDrive.client_side.gui import screens
from OpenDrive.client_side.od_logging import logger_gui


class ScreenRegistration(Screen):

    tf_username = ObjectProperty(None)
    tf_email = ObjectProperty(None)
    tf_password = ObjectProperty(None)
    tf_repeated_password = ObjectProperty(None)
    lbl_user_hints = ObjectProperty(None)

    def btn_release_register(self):
        username = self.tf_username.text
        email = self.tf_email.text
        password = self.tf_password.text
        repeated_password = self.tf_repeated_password.text

        if len(username) == 0 or len(password) == 0:
            self.show_error_message("Please fill all fields")
            return

        if not is_valid_email(email) and len(email) != 0:
            self.show_error_message("Please fill in a valid email address")
            self.tf_email.text = ""
            return

        if password != repeated_password:
            self.show_error_message("Passwords are not equal")
            self.tf_password.text = ""
            self.tf_repeated_password.text = ""
            return

        status = interface.register(username, password, email)
        if status.was_successful():
            logger_gui.info("Successfully registered")
            screens.screen_manager.do_login()
        else:
            logger_gui.info(f"Failed to register: {status.get_text()}")
            self.show_error_message(status.get_text())

    def btn_release_login(self):
        screens.screen_manager.set_screen(screens.LOGIN_MANUAL)

    def show_error_message(self, message: str):
        self.lbl_user_hints.color[3] = 1
        self.lbl_user_hints.text = message


def is_valid_email(email):
    if len(email) > 7:
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            return True
    return False
