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
import os
import re

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
from OpenDrive.client_side import merge_folders


class PopupConfigFolder(Popup):

    tf_client_path: TextInput = ObjectProperty(None)
    tf_server_path: TextInput = ObjectProperty(None)

    tf_include_files: TextInput = ObjectProperty(None)
    tf_include_folders: TextInput = ObjectProperty(None)
    tf_include_advanced: TextInput = ObjectProperty(None)

    tf_exclude_files: TextInput = ObjectProperty(None)
    tf_exclude_folders: TextInput = ObjectProperty(None)
    tf_exclude_advanced: TextInput = ObjectProperty(None)

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
        is_valid_data = self._validate_data()
        if is_valid_data:
            if self._edit_existing:
                logger.warning("Editing folders is not implemented yet.")
                self.show_error_message("Editing folders is not implemented yet.")
            else:
                abs_local_path = normalize_path(self.tf_client_path.text)
                server_path = normalize_path(self.tf_server_path.text)
                status = interface.add_sync_folder(abs_local_path, server_path)
                if status.was_successful():
                    self.dismiss()
                    self._synchronizations_container.update_folders_on_added(abs_local_path)
                else:
                    logger.warning(status.get_text())
                    self.show_error_message(status.get_text())

    def btn_release_cancel(self):
        self.dismiss()

    def _validate_data(self) -> bool:
        validate_methods = [self._validate_paths]
        for validation in validate_methods:
            is_valid = validation()
            if not is_valid:
                return False
        return True

    def _validate_paths(self) -> bool:
        client_path = normalize_path(self.tf_client_path.text)
        server_path = self.tf_server_path.text
        if not os.path.exists(client_path):
            self.show_error_message("Local path must exist already!")
            return False
        invalid_signs = [":", "*", "?", "/", "\\", "\"", "<", ">", "|"]
        if sum([1 if sign in server_path else 0 for sign in invalid_signs]):
            self.show_error_message(f"Invalid server path! Following signs are not allowed: {invalid_signs}")
            return False
        return True

    def _validate_patterns(self):
        pass

    def show_error_message(self, message: str):
        logger.debug(f"ERROR message: {message}")
        return
        self.lbl_user_hints.color[3] = 1
        self.lbl_user_hints.text = message


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


class MergeMethods(BoxLayout):

    dropdown = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_dropdown(self, *args):
        for method in merge_folders.ALL_METHODS:
            self.dropdown.add_widget(MergeMethodItem(self, text=method.NAME))

    def set_method(self, merge_method_item: 'MergeMethodItem'):
        self.dropdown.select(merge_method_item.text)


class MergeMethodItem(Button):

    def __init__(self, container: MergeMethods, **kwargs):
        super().__init__(**kwargs)
        self.container = container

    def on_release(self):
        self.container.set_method(self)