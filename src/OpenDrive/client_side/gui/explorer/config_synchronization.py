"""
:module: OpenDrive.
:synopsis: 
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
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput

from OpenDrive.client_side import interface
from OpenDrive.client_side.gui.explorer.desktop_file_dialogs import Desktop_FolderDialog
from OpenDrive.client_side.gui.explorer import synchronizations
from OpenDrive.general.paths import NormalizedPath, normalize_path
from OpenDrive.client_side.od_logging import logger


class PopupConfigFolder(Popup):
    tf_client_path: TextInput = ObjectProperty(None)
    tf_server_path: TextInput = ObjectProperty(None)
    btn_save_add: Button = ObjectProperty(None)

    def __init__(self, synchronizations_container: synchronizations.Synchronizations, edit_existing: bool, **kwargs):
        super().__init__(**kwargs)
        self._synchronizations_container = synchronizations_container
        self._edit_existing = edit_existing
        if edit_existing:
            self.btn_save_add.text = "Save"

    def set_data(self, client_path=None, server_path=None, include_regexes=None, exclude_regexes=None):
        if client_path:
            self.tf_client_path.text = client_path
        if server_path:
            self.tf_server_path.text = server_path

    def btn_release_add(self):
        if self._edit_existing:
            logger.warning("Editing folders is not implemented yet.")
        else:
            abs_local_path = normalize_path(self.tf_client_path.text)
            server_path = normalize_path(self.tf_server_path.text)
            status = interface.add_sync_folder(abs_local_path, server_path)
            if status.was_successful():
                self.dismiss()
                self._synchronizations_container.update_folders_on_added(abs_local_path)
            else:
                logger.warning(status.get_text())
                # TODO: transmit message to user

    def dummy(self, *args):
        logger.debug(self.tf_server_path.text)
        logger.debug(self.tf_client_path.text)


class Path(BoxLayout):

    tf_path: TextInput = ObjectProperty(None)
    browse = ObjectProperty(None)

    def browse_client_path(self):
        Desktop_FolderDialog(
            title="Select Folder",
            initial_directory="",
            on_accept=lambda folder_path: self.set_path(folder_path),
            on_cancel=lambda: -1,
        ).show()

    def set_path(self, path: str):
        self.tf_path.text = normalize_path(path)

    def browse_server_path(self):
        status, all_server_folders = interface.get_all_remote_folders()
        if status.was_successful():
            popup_server_folders = PopupBrowseServerFolder(self)
            popup_server_folders.foldersView.set_folders(all_server_folders)
            popup_server_folders.open()
        else:
            logger.warning(status.get_text())
            # TODO: transmit message to user


class FoldersView(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path: str = ""

    def update_selected_path(self, path: str):
        self.selected_path = path

    def set_folders(self, folders: list):
        self.data = [{"text": folder} for folder in folders]


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected
        if is_selected:
            rv.update_selected_path(rv.data[index]["text"])


class PopupBrowseServerFolder(Popup):
    foldersView: FoldersView = ObjectProperty(None)

    def __init__(self, paths_container: Path, **kwargs):
        super().__init__(**kwargs)
        self.paths_container = paths_container

    def set_server_path(self):
        path = self.foldersView.selected_path
        self.paths_container.set_path(path)
        self.dismiss()
