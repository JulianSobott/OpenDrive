"""
@author: Julian Sobott
@brief: Tracks changes to files in all defined folders.
@description:

@external_use:

@internal_use:
"""
from typing import List
from watchdog import events as watchdog_events, observers as watchdog_observers

from OpenDrive.client_side.Logging import logger

observer = watchdog_observers.Observer()
all_watchers = []


def start(all_folders_to_sync: List[str]):
    """Start watching at all folders in a new thread."""
    pass


def start_observing():
    observer.start()


def stop_observing():
    observer.unschedule_all()
    observer.stop()


def add_watcher(abs_folder_path: str, ignore_patterns: List[str] = ()):
    event_handler = FileSystemEventHandler(abs_folder_path, ignore_patterns)
    observer.schedule(event_handler, abs_folder_path, recursive=True)
    all_watchers.append(event_handler)


class FileSystemEventHandler(watchdog_events.PatternMatchingEventHandler):

    def __init__(self, abs_folder_path, ignore_patterns: List[str] = ()):
        super().__init__(ignore_patterns=ignore_patterns)
        self.folder_path = abs_folder_path

    def on_any_event(self, event):
        logger.debug(event)

    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass
