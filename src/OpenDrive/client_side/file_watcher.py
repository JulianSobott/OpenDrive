"""
@author: Julian Sobott
@brief: Tracks changes to files in all defined folders.
@description:

@external_use:

@internal_use:
"""
import os
from typing import List
from watchdog import events as watchdog_events, observers as watchdog_observers

from OpenDrive.client_side.Logging import logger
from OpenDrive.client_side import database

observer = watchdog_observers.Observer()

def start(all_folders_to_sync: List[str]):
    """Start watching at all folders in a new thread."""
    pass


def start_observing():
    observer.start()


def stop_observing():
    observer.stop()
    observer.__init__()


def add_watcher(abs_folder_path: str, ignore_patterns: List[str] = (), folder_id: int = None):
    if folder_id is None:
        sync_folder = database.SyncFolder.from_path(abs_folder_path)
        folder_id = sync_folder.id
    event_handler = FileSystemEventHandler(abs_folder_path, folder_id, ignore_patterns)
    observer.schedule(event_handler, abs_folder_path, recursive=True)


class FileSystemEventHandler(watchdog_events.RegexMatchingEventHandler):

    def __init__(self, abs_folder_path: str, folder_id: int, ignore_patterns: List[str] = ()):
        super().__init__(ignore_regexes=ignore_patterns, case_sensitive=False)
        self.folder_path = abs_folder_path
        self._folder_id: int = folder_id

    def on_any_event(self, event):
        """Known issue with watchdog: When a folder is created it checks after 1 second, if there are other files inside
        this folder. If there are any files and folders (uses os.walk()) they are added 'manually' as creation events.
        This is necessary, because when the folder is pasted, the inner files are not added. The issue occurs when a
        folder and inner files/folders are created (e.g. from python). Then these files/folders are handled twice.
        Once the manual and once the normal on create way. To solve this unique errors at insert are ignored in the DB.
        """
        logger.debug(f"{event.event_type}: {os.path.relpath(event.src_path, self.folder_path)}")

    def on_created(self, event):
        is_dir = event.is_directory
        src_path = event.src_path
        rel_path = os.path.relpath(src_path, self.folder_path)
        database.Change.create(self._folder_id, rel_path, is_folder=is_dir, is_created=True)

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass
