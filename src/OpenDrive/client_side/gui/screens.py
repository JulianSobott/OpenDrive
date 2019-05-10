from typing import NewType

__all__ = ["ScreenManager", "screen_manager", "LOGIN_MANUAL", "EXPLORER"]


ScreenName = NewType("ScreenName", str)

LOGIN_MANUAL = ScreenName("login_manual_screen")
EXPLORER = ScreenName("explorer")


class ScreenManager:

    def __init__(self, app):
        self.app = app

    def set_screen(self, screen_name: ScreenName):
        self.app.root.current = screen_name


screen_manager: ScreenManager = None    # This will be set in main.py
