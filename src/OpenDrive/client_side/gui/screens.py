from typing import NewType

__all__ = ["ScreenManager", "screen_manager", "LOGIN_MANUAL", "EXPLORER"]


ScreenName = NewType("ScreenName", str)

LOGIN_MANUAL = ScreenName("screen_login_manual")
REGISTRATION = ScreenName("screen_registration")
EXPLORER = ScreenName("screen_explorer")


class ScreenManager:

    def __init__(self, app):
        self.app = app

    def set_screen(self, screen_name: ScreenName):
        self.app.root.current = screen_name

    def do_login(self):
        """Action, when the user is successfully authenticated. If only a authentication was needed, the app is
        closed."""
        if self.app.authentication_only:
            self.app.stop()
        else:
            self.set_screen(EXPLORER)


screen_manager: ScreenManager = None    # This will be set in main.py
