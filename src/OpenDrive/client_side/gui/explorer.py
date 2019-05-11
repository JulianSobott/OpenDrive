from kivy.uix.button import Button

from OpenDrive.client_side.gui import screens


class BtnBack(Button):

    def on_release(self):
        screens.screen_manager.set_screen(screens.LOGIN_MANUAL)

