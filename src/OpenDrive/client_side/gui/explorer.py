from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from OpenDrive.client_side import file_changes_json as changes
from OpenDrive.client_side.od_logging import logger


class ScreenExplorer(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box_folders_container = BoxLayout(orientation="vertical")
        self.add_widget(box_folders_container)
        self.folders = changes.get_all_data()
        for path, folder in self.folders.items():
            lbl_folder = Label(text=path)
            box_folders_container.add_widget(lbl_folder)
