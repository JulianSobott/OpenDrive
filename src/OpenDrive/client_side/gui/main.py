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
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget


class ScreenLoginManual(Screen):
    pass


class ScreenRegister(Screen):
    pass


class ScreenExplorer(Screen):
    pass


class BtnLoginManual(Button):

    def on_release(self):
        OpenDriveApp.screen_manager.current = "screen_explorer"


class OpenDriveApp(App):
    screen_manager = ScreenManager()

    def build(self):
        self.screen_manager.switch_to(ScreenLoginManual())
        OpenDriveApp.screen_manager.add_widget(ScreenLoginManual(name="screen_login_manual"))
        OpenDriveApp.screen_manager.add_widget(ScreenExplorer(name="screen_explorer"))
        OpenDriveApp.screen_manager.current = "screen_login_manual"
        return self.screen_manager


def main():
    OpenDriveApp().run()


if __name__ == '__main__':
    main()