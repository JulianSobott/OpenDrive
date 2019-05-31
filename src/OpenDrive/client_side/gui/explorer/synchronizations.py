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
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

from OpenDrive.client_side import interface


class Synchronizations(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.folders = interface.get_sync_data()
        self.data = [{'local_path': str(path), 'remote_path': str(folder["server_folder_path"])} for path, folder in
                     self.folders.items()]


class SynchronizationContainer(BoxLayout):

    local_path = ""
    remote_path = ""

    lbl_local_path: Label = ObjectProperty(None)
    lbl_remote_path: Label = ObjectProperty(None)

    def do_layout(self, *largs):
        super().do_layout(*largs)
        self.lbl_local_path.text = self.local_path
        self.lbl_remote_path.text = self.remote_path
