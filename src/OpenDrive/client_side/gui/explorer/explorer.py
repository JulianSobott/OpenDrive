from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from kivy.uix.screenmanager import Screen

from OpenDrive.client_side.gui.explorer import synchronizations
from OpenDrive.client_side.gui.explorer import config_synchronization


class ScreenExplorer(Screen):

    btn_add_synchronization: Button = ObjectProperty(None)
    synchronizations_container: synchronizations.Synchronizations = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_btn_add_synchronization(self, *args):
        self.btn_add_synchronization.bind(on_release=self.btn_release_add_synchronization)

    def btn_release_add_synchronization(self, button):
        popup = config_synchronization.PopupConfigFolder(self.synchronizations_container, edit_existing=False)
        popup.open()
