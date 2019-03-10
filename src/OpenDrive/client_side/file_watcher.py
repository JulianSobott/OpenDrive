"""
@author: Julian Sobott
@brief: Tracks changes to files in all defined folders.
@description:

@external_use:

@internal_use:
"""
from typing import List
from watchdog import events as watchdog_events


def start(all_folders_to_sync: List[str]):
    """Start watching at all folders in a new thread."""
    pass


class FileSystemEventHandler(watchdog_events.PatternMatchingEventHandler):

    def __init__(self, abs_folder_path, ignore_patterns: List[str] = ()):
        super().__init__(ignore_patterns=ignore_patterns)
        self.folder_path = abs_folder_path

    def on_any_event(self, event):
        pass

    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass
