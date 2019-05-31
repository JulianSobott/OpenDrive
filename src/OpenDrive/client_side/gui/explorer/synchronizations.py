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


class Synchronizations(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'local_path': str(x), 'remote_path': str(x)} for x in range(100)]


class SynchronizationContainer(BoxLayout):

    local_path = ""
    remote_path = ""

    lbl_local_path: Label = ObjectProperty(None)
    lbl_remote_path: Label = ObjectProperty(None)

    def do_layout(self, *largs):
        super().do_layout(*largs)
        self.lbl_local_path.text = self.local_path
        self.lbl_remote_path.text = self.remote_path
