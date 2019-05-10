from kivy.uix.button import Button

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger


class BtnLogin(Button):

    def on_release(self):
        username = ""
        password = ""
        status = interface.login_manual(username, password)
        if status.was_successful() or True:
            logger.debug("Successfully logged in")
            window.set_screen("screen_explorer")
        else:
            logger.debug("Login failed TODO")
            logger.debug(status.get_text())


class Window:

    def __init__(self):
        self.app = None

    def set_screen(self, screen_name: str):
        self.app.root.current = screen_name


window = Window()
