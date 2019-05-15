from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from OpenDrive.client_side import interface
from OpenDrive.general import paths as gen_paths
from OpenDrive.client_side.gui.desktop_file_dialogs import Desktop_FolderDialog
from OpenDrive.client_side.od_logging import logger



class ScreenExplorer(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folders = interface.get_sync_data()

        self.box_folders_container = BoxLayout(orientation="vertical")
        self.add_widget(self.box_folders_container)
        self.folder_containers = {}
        for path, folder in self.folders.items():
            self._add_folder(path, folder)
        self.box_folders_container.add_widget(BtnAddSynchronization(self))

    def _add_folder(self, path: str, folder: dict):
        """local_path, server_path, status, expand, edit, delete"""
        box_folder = BoxLayout(orientation="horizontal")

        lbl_local_path = Label(text=path)
        box_folder.add_widget(lbl_local_path)

        lbl_server_path = Label(text=str(folder["server_folder_path"]))
        box_folder.add_widget(lbl_server_path)

        lbl_status = Label(text="Ok")
        box_folder.add_widget(lbl_status)

        btn_expand = Button(text="expand")
        box_folder.add_widget(btn_expand)

        btn_edit = Button(text="edit")
        box_folder.add_widget(btn_edit)

        btn_delete = Button(text="delete", on_release=partial(self.btn_release_remove_sync_folder, path))
        box_folder.add_widget(btn_delete)

        self.box_folders_container.add_widget(box_folder)
        self.folder_containers[path] = box_folder

    def btn_release_remove_sync_folder(self, folder_path: gen_paths.NormalizedPath, button):
        interface.remove_synchronization(folder_path)
        self.box_folders_container.clear_widgets([self.folder_containers[folder_path]])

    def btn_release_add_synchronization(self, button):
        popup = PopupConfigFolder(self)
        popup.open()


class BtnAddSynchronization(Button):

    def __init__(self, explorer_screen, **kwargs):
        super().__init__(**kwargs)
        self._explorer: ScreenExplorer = explorer_screen


class PopupConfigFolder(Popup):

    tf_client_path = ObjectProperty(None)
    tf_server_path = ObjectProperty(None)

    def __init__(self, explorer, **kwargs):
        super().__init__(**kwargs)
        self._explorer = explorer

    def browse_client_path(self):
        Desktop_FolderDialog(
            title="Select Folder",
            initial_directory="",
            on_accept=lambda folder_path: self.set_client_path(folder_path),
            on_cancel=lambda: -1,
        ).show()

    def set_client_path(self, path: str):
        self.tf_client_path.text = path

    def browse_server_path(self):
        pass
