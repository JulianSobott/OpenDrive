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
from kivy.lang import Builder

from OpenDrive.client_side.gui import login_manual


class BtnSwitch(Button):

    def on_press(self):
        app.root.current = "screen_login_manual"


class OpenDriveApp(App):
    pass


app = OpenDriveApp()


def main():
    app.run()


if __name__ == '__main__':
    main()