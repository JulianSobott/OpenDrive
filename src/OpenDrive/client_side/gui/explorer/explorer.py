from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from kivy.uix.screenmanager import Screen

from OpenDrive.client_side.gui.explorer import synchronizations
from OpenDrive.client_side.gui.explorer import config_synchronization


class ScreenExplorer(Screen):

    btn_add_synchronization: Button = ObjectProperty(None)
    synchronizations_container: synchronizations.Synchronizations = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_btn_add_synchronization(self, *args):
        self.btn_add_synchronization.bind(on_release=self.btn_release_add_synchronization)

    def btn_release_add_synchronization(self, button):
        popup = config_synchronization.PopupConfigFolder(self.synchronizations_container, edit_existing=False)
        popup.open()


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
