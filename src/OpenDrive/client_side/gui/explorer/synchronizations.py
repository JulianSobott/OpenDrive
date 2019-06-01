"""
:module: OpenDrive.client_side.gui.explorer.synchronizations
:synopsis: A list of all synchronizations
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
from functools import partial

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

from OpenDrive.client_side import interface
from OpenDrive.client_side.od_logging import logger


class Synchronizations(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folders = interface.get_sync_data()
        self.data = [{'local_path': str(path), 'remote_path': str(folder["server_folder_path"]),
                      "synchronizations_container": self}
                     for path, folder in self.folders.items()]

    def remove_synchronization(self, local_path: str):
        for i in range(len(self.data)):
            if self.data[i]['local_path'] == local_path:
                interface.remove_synchronization(local_path)
                self.data.pop(i)
                break
        print(self.data)


class SynchronizationContainer(BoxLayout):

    local_path = ObjectProperty("")
    remote_path = ObjectProperty("")
    synchronizations_container: Synchronizations = ObjectProperty(None)

    lbl_local_path: Label = ObjectProperty(None)
    lbl_remote_path: Label = ObjectProperty(None)
    btn_delete: Button = ObjectProperty(None)

    def release_btn_delete(self):
        self.synchronizations_container.remove_synchronization(self.local_path)