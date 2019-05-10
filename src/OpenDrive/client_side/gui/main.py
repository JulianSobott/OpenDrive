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


class MetaSingletonApp(type):

    _instance = None

    def __call__(cls, *args, **kwargs) -> 'OpenDriveApp':
        if cls._instance is None:
            cls._instance = super(MetaSingletonApp, cls).__call__(*args, **kwargs)
        return cls._instance


class OpenDriveApp(App):
    pass


def set_screen(screen_name: str):
        app.root.current = screen_name


def main():
    app.run()


app = OpenDriveApp()
login_manual.window.app = app
print(id(app))
print(id(MetaSingletonApp))

if __name__ == '__main__':
    main()