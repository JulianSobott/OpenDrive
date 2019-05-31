from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from functools import partial

from kivy.uix.textinput import TextInput

from OpenDrive.client_side import interface
from OpenDrive.general import paths as gen_paths
from client_side.gui.explorer.desktop_file_dialogs import Desktop_FolderDialog
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

        btn_edit = Button(text="edit", on_release=partial(self.btn_release_edit_synchronization, path))
        box_folder.add_widget(btn_edit)

        btn_delete = Button(text="delete", on_release=partial(self.btn_release_remove_sync_folder, path))
        box_folder.add_widget(btn_delete)

        self.box_folders_container.add_widget(box_folder)
        self.folder_containers[path] = box_folder

    def btn_release_remove_sync_folder(self, folder_path: gen_paths.NormalizedPath, button):
        interface.remove_synchronization(folder_path)
        self.box_folders_container.clear_widgets([self.folder_containers[folder_path]])

    def btn_release_add_synchronization(self, button):
        popup = PopupConfigFolder(self, edit_existing=False)
        popup.open()

    def update_folders_on_added(self, folder_path: str):
        """Call this when a new folder is added from the popup window."""
        all_folders = interface.get_sync_data()
        folder_path = gen_paths.normalize_path(folder_path)
        self._add_folder(folder_path, all_folders[folder_path])

    def btn_release_edit_synchronization(self, folder_path, button):
        data = interface.get_sync_data()
        folder_data = data[folder_path]
        popup = PopupConfigFolder(self, edit_existing=True)
        popup.open()
        popup.set_data(client_path=folder_path, server_path=folder_data["server_folder_path"])


class BtnAddSynchronization(Button):

    def __init__(self, explorer_screen, **kwargs):
        super().__init__(**kwargs)
        self._explorer: ScreenExplorer = explorer_screen


class PopupConfigFolder(Popup):

    tf_client_path: TextInput = ObjectProperty(None)
    tf_server_path: TextInput = ObjectProperty(None)
    btn_save_add: Button = ObjectProperty(None)

    def __init__(self, explorer, edit_existing: bool, **kwargs):
        super().__init__(**kwargs)
        self._explorer: ScreenExplorer = explorer
        self._edit_existing = edit_existing
        if edit_existing:
            self.btn_save_add.text = "Save"

    def set_data(self, client_path=None, server_path=None, include_regexes=None, exclude_regexes=None):
        if client_path:
            self.tf_client_path.text = client_path
        if server_path:
            self.tf_server_path.text = server_path

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
        status, all_server_folders = interface.get_all_remote_folders()
        if status.was_successful():
            popup_server_folders = PopupBrowseServerFolder(self)
            popup_server_folders.foldersView.set_folders(all_server_folders)
            popup_server_folders.open()
        else:
            logger.warning(status.get_text())
            # TODO: transmit message to user

    def btn_release_add(self):
        if self._edit_existing:
            logger.warning("Editing folders is not implemented yet.")
        else:
            abs_local_path = self.tf_client_path.text
            server_path = self.tf_server_path.text
            status = interface.add_sync_folder(abs_local_path, server_path)
            if status.was_successful():
                self.dismiss()
                self._explorer.update_folders_on_added(abs_local_path)
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

    def __init__(self, popup_config: PopupConfigFolder, **kwargs):
        super().__init__(**kwargs)
        self.popup_config = popup_config

    def set_server_path(self):
        path = self.foldersView.selected_path
        self.popup_config.tf_server_path.text = path
        self.dismiss()


# TODO: For some reason the program crashes when the following line is added: `from kivy.uix.dropdown import DropDown`
# class DropDownMergeMethods(kivy.uix.dropdown.DropDown):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         merge_methods = merge_folders.MergeMethods
#         self.add_widget(BtnMergeMethod(merge_methods.TAKE_1, self))
#         self.add_widget(BtnMergeMethod(merge_methods.TAKE_2, self))
#         self.add_widget(BtnMergeMethod(merge_methods.COMPLETE_BOTH, self))
#         self.add_widget(BtnMergeMethod(merge_methods.CONFLICTS, self))
#         self.add_widget(BtnMergeMethod(merge_methods.PRIORITIZE_1, self))
#         self.add_widget(BtnMergeMethod(merge_methods.PRIORITIZE_2, self))
#         self.add_widget(BtnMergeMethod(merge_methods.PRIORITIZE_LATEST, self))
#
#
# class BtnMergeMethod(Button):
#
#     def __init__(self, merge_method, dropdown, **kwargs):
#         super().__init__(text=str(merge_method), **kwargs)
#         self.dropdown: DropDownMergeMethods = dropdown
#         self.merge_method = merge_method
#
#     def on_release(self):
#         self.dropdown.select(self.text)
