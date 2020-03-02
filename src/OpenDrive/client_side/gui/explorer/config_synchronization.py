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
from typing import Tuple, List

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
from OpenDrive.client_side.gui.explorer import synchronizations
from OpenDrive.client_side.gui.explorer import pattern_parser
from OpenDrive.general.paths import NormalizedPath, normalize_path
from OpenDrive.client_side.od_logging import logger_gui
from OpenDrive.client_side import merge_folders
from OpenDrive.client_side.gui.explorer import desktop_file_dialogs


class PopupConfigFolder(Popup):

    tf_client_path: TextInput = ObjectProperty(None)
    tf_server_path: TextInput = ObjectProperty(None)

    tf_include: TextInput = ObjectProperty(None)
    tf_exclude: TextInput = ObjectProperty(None)

    merge_methods: 'MergeMethods' = ObjectProperty(None)

    btn_save_add: Button = ObjectProperty(None)

    def __init__(self, synchronizations_container: synchronizations.Synchronizations, edit_existing: bool, **kwargs):
        super().__init__(**kwargs)
        self._synchronizations_container = synchronizations_container
        self._edit_existing = edit_existing
        if edit_existing:
            self.btn_save_add.text = "Save"

        self._is_valid_data = True
        self._error_message = ""

    def set_data(self, client_path: str = None, server_path: str = None, include_patterns: str = None,
                 exclude_patterns: str = None):
        if client_path:
            self.tf_client_path.text = client_path
        if server_path:
            self.tf_server_path.text = server_path

        if include_patterns:
            self.tf_server_path.text = include_patterns

        if exclude_patterns:
            self.tf_server_path.text = exclude_patterns

    def btn_release_add(self):
        self._is_valid_data = True
        client_path, server_path = self.get_valid_paths()
        include_regexes, exclude_regexes = self.get_valid_patterns()
        merge_method = self.get_valid_merge_method()
        if self._is_valid_data:
            status = interface.add_sync_folder(client_path, server_path, include_regexes, exclude_regexes,
                                               merge_method)
            if status.was_successful():
                logger_gui.info("Successfully added new synchronization")
                self.dismiss()
                self._synchronizations_container.update_folders_on_added(client_path)
            else:
                logger_gui.info(f"Failed to add new synchronization: {status.get_text()}")
                self.show_error_message(status.get_text())
        else:
            logger_gui.info(f"Invalid data entered (Add sync to folder): {self._error_message}")
            self.show_error_message(self._error_message)

    def btn_release_cancel(self):
        self.dismiss()

    def get_valid_paths(self):
        def failure(msg):
            self._error_message = msg
            self._is_valid_data = False
            return "", ""
        client_path = self.tf_client_path.text
        server_path = self.tf_server_path.text
        if len(server_path) == 0 or len(client_path) == 0:
            return failure("Please fill both paths!")
        client_path = normalize_path(client_path)
        server_path = normalize_path(server_path)
        if not os.path.exists(client_path):
            return failure("Local path must exist already!")

        # try to validate server path
        server_max_length = 255
        if len(server_path) > server_max_length:
            return failure(f"Server path is too long. Max length is {server_max_length}")
        max_sub_folders = 10
        if server_path.count("/") > max_sub_folders:
            return failure(f"Server path contains too many folders. Max number is {max_sub_folders}")
        return client_path, server_path

    def get_valid_patterns(self) -> Tuple[List[str], List[str]]:
        include_patterns = self.tf_include.text
        exclude_patterns = self.tf_exclude.text
        if len(include_patterns.strip()) > 0:
            include_regexes = pattern_parser.parse_patterns(include_patterns)
        else:
            include_regexes = [".*"]
        if len(exclude_patterns.strip()) > 0:
            exclude_regexes = pattern_parser.parse_patterns(exclude_patterns)
        else:
            exclude_regexes = []
        return include_regexes, exclude_regexes

    def get_valid_merge_method(self):
        if self.does_server_folder_exist():
            return self.merge_methods.selected_merge_method
        else:
            return merge_folders.MergeMethods.TAKE_1

    def does_server_folder_exist(self):
        return self.tf_server_path in interface.get_all_remote_folders()

    def show_error_message(self, message: str):
        # TODO: check if it works
        self.lbl_user_hints.color[3] = 1
        self.lbl_user_hints.text = message


class Path(BoxLayout):

    tf_path: TextInput = ObjectProperty(None)
    browse = ObjectProperty(None)

    def browse_client_path(self):
        path = desktop_file_dialogs.get_directory_path("Please select a directory for synchronization")
        logger_gui.debug(f"User selected path for synchronization: path={path}")
        self.set_path(path)

    def set_path(self, path: str):
        self.tf_path.text = normalize_path(path)

    def browse_server_path(self):
        status, all_server_folders = interface.get_all_remote_folders()
        if status.was_successful():
            popup_server_folders = PopupBrowseServerFolder(self)
            popup_server_folders.foldersView.set_folders(all_server_folders)
            popup_server_folders.open()
        else:
            logger_gui.warning(status.get_text())
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
        self.selected_merge_method = merge_folders.MergeMethods.DEFAULT
        self.names_methods = {method.NAME: method for method in merge_folders.ALL_METHODS}

    def on_dropdown(self, *args):
        for method in merge_folders.ALL_METHODS:
            self.dropdown.add_widget(MergeMethodItem(self, text=method.NAME))

    def set_method(self, merge_method_item: 'MergeMethodItem'):
        self.dropdown.select(merge_method_item.text)
        self.selected_merge_method = self.names_methods[merge_method_item.text]


class MergeMethodItem(Button):

    def __init__(self, container: MergeMethods, **kwargs):
        super().__init__(**kwargs)
        self.container = container

    def on_release(self):
        self.container.set_method(self)
