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

from OpenDrive.client_side.gui import screens

# DO NOT DELETE UNUSED IMPORTS!
# They are needed inside the OpenDriveApp
from OpenDrive.client_side.gui import login_manual
from OpenDrive.client_side.gui import explorer


class OpenDriveApp(App):
    pass


def main():
    app.run()


app = OpenDriveApp()
screens.screen_manager = screens.ScreenManager(app)

if __name__ == '__main__':
    main()