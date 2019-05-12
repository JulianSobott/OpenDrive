from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger


class ScreenExplorer(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_folders_container = BoxLayout(orientation="vertical")
        self.add_widget(self.box_folders_container)
        self.folders = interface.get_sync_data()
        for path, folder in self.folders.items():
            self._add_folder(path, folder)

    def _add_folder(self, path: str, folder: dict):
        """local_path, server_path, status, expand, edit, delete"""
        box_folder = BoxLayout(orientation="horizontal")

        lbl_local_path = Label(text=path)
        box_folder.add_widget(lbl_local_path)

        lbl_server_path = Label(text=folder["server_folder_path"])
        box_folder.add_widget(lbl_server_path)

        lbl_status = Label(text="Ok")
        box_folder.add_widget(lbl_status)

        btn_expand = Button(text="expand")
        box_folder.add_widget(btn_expand)

        btn_edit = Button(text="edit")
        box_folder.add_widget(btn_edit)

        btn_delete = Button(text="delete")
        box_folder.add_widget(btn_delete)

        self.box_folders_container.add_widget(box_folder)
