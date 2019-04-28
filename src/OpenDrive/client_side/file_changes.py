"""
:module: OpenDrive.client_side.file_watcher
:synopsis: Tracks changes to files in all defined folders.
:author: Julian Sobott

public functions
----------------

.. autofunction:: start

private functions
-----------------

.. autofunction:: start_observing

.. autofunction:: add_watcher

.. autofunction:: start_observing

.. autofunction:: stop_observing

private classes
---------------

.. autoclass:: FileSystemEventHandler
    :members:
    :show-inheritance:

"""
import os
from typing import List, Dict, Tuple
from watchdog import events as watchdog_events, observers as watchdog_observers
from watchdog.observers.api import ObservedWatch
import datetime

from OpenDrive.client_side.od_logging import logger
from OpenDrive.client_side import paths, file_changes_json

from OpenDrive.general.paths import normalize_path, NormalizedPath

observer = watchdog_observers.Observer()
watchers: Dict[NormalizedPath, Tuple['FileSystemEventHandler', ObservedWatch]] = {}

__all__ = ["start", "add_folder", "remove_folder_from_watching"]


def start() -> None:
    """Start watching at all folders in a new thread. Calling this is enough and no further function calls inside this
    module are needed."""
    all_folders = file_changes_json.get_all_synced_folders()
    for folder in all_folders:
        add_watcher(folder["folder_path"], folder["include_regexes"], folder["exclude_regexes"])
    observer.start()


def add_folder(abs_folder_path: str, include_regexes: List[str] = (".*",), exclude_regexes: List[str] = ()) -> bool:
    """If possible add folder to file and start watching. Returns True, if the folder was added."""
    assert isinstance(include_regexes, list) or isinstance(include_regexes, tuple)
    assert isinstance(exclude_regexes, list) or isinstance(exclude_regexes, tuple)
    abs_folder_path = normalize_path(abs_folder_path)
    added = file_changes_json.add_folder(abs_folder_path, include_regexes, exclude_regexes)
    if not added:
        return False
    add_watcher(abs_folder_path, include_regexes, exclude_regexes)


def remove_folder_from_watching(abs_folder_path: str) -> None:
    """Stops watching at the folder and removes it permanently from the json file"""
    norm_folder_path = normalize_path(abs_folder_path)
    _remove_watcher(norm_folder_path)
    file_changes_json.remove_folder(norm_folder_path)


def add_single_ignores(abs_folder_path: str, rel_paths: List[str]) -> None:
    """Add folder and file names that shall be ignored, because they are pulled from the server."""
    norm_folder_path = normalize_path(abs_folder_path)
    assert norm_folder_path in watchers.keys(), f"No event_handler, watches at the specified folder: {norm_folder_path}"
    event_handler, _ = watchers[norm_folder_path]
    event_handler.add_single_ignores(rel_paths)


def add_permanent_ignores(ignores: List[str], folder_id: int = None, abs_folder_path: str = None) -> None:
    assert abs_folder_path is not None or folder_id is not None, "One of both arguments must be not None."
    if folder_id is None:
        folder_id = database.SyncFolder.from_path(abs_folder_path)

    seq = [(folder_id, pattern, True) for pattern in ignores]
    with database.DBConnection(paths.LOCAL_DB_PATH) as db:
        sql = 'INSERT INTO "ignores" (' \
              '"folder_id", "pattern", "sub_folders") ' \
              'VALUES (?, ?, ?)'
        db.cursor.executemany(sql, seq)


def remove_permanent_ignores(ignores: List[str], folder_id: int = None, abs_folder_path: str = None) -> None:
    assert abs_folder_path is not None or folder_id is not None, "One of both arguments must be not None."
    if folder_id is None:
        folder_id = database.SyncFolder.from_path(abs_folder_path)
    with database.DBConnection(paths.LOCAL_DB_PATH) as db:
        sql = f"DELETE FROM ignores WHERE folder_id = ? and pattern in ({','.join(['?'] * len(ignores))})"
        db.delete(sql, (folder_id, *ignores))


def _exist_folder(abs_folder_path: str) -> bool:
    if not os.path.exists(abs_folder_path):
        return False
    return True


def _add_folder_to_db(abs_folder_path: str) -> int:
    folder_id = database.SyncFolder.create(abs_folder_path)
    return folder_id


def _add_ignores_to_db(ignore_patterns: List[str]) -> None:
    pass


def start_observing():
    """Protects the `observer` from external access"""
    observer.start()


def stop_observing():
    global watchers
    """Protects the `observer` from external access"""
    observer.stop()
    watchers = {}
    observer.__init__()


def add_watcher(abs_folder_path: str, include_regexes: List[str] = (".*",), exclude_regexes: List[str] = ()):
    """Watcher, that handles changes to the specified folder."""
    event_handler = FileSystemEventHandler(abs_folder_path, include_regexes, exclude_regexes)
    watch = observer.schedule(event_handler, abs_folder_path, recursive=True)
    watchers[abs_folder_path] = event_handler, watch


def _remove_watcher(abs_folder_path: NormalizedPath):
    """Stops watching"""
    event_handler, watch = watchers.pop(abs_folder_path)
    observer.remove_handler_for_watch(event_handler, watch)
    observer.unschedule(watch)


class FileSystemEventHandler(watchdog_events.RegexMatchingEventHandler):
    """Track changes inside a folder. Every change will either create a new entry in the `changes` table or change
    an existing one.
    It is possible to exclude (don't handle) respectively include certain regex patterns. Whereby exclude patterns
    are 'stronger' than include."""

    def __init__(self, abs_folder_path: NormalizedPath, include_regexes: List[str] = (".*",),
                 exclude_regexes: List[str] = ()):
        super().__init__(regexes=include_regexes, ignore_regexes=exclude_regexes, case_sensitive=False)
        self.folder_path = abs_folder_path
        self._single_ignore_paths: Dict[NormalizedPath, Tuple[datetime.datetime, bool]] = {}
        self._is_dir: bool = False
        self._rel_path: NormalizedPath = normalize_path("")
        self._ignore = False

    def on_any_event(self, event):
        """Known issue with watchdog: When a folder is created it checks after 1 second, if there are other files inside
        this folder. If there are any files and folders (uses os.walk()) they are added 'manually' as creation events.
        This is necessary, because when the folder is pasted, the inner files are not added. The issue occurs when a
        folder and inner files/folders are created (e.g. from python). Then these files/folders are handled twice.
        Once the manual and once the normal on create way. To solve this unique errors at insert are ignored in the DB.
        """
        logger.debug(f"{event.event_type}: {os.path.relpath(event.src_path, self.folder_path)}")
        # Metadata
        self._is_dir = event.is_directory
        src_path = event.src_path
        self._rel_path = normalize_path(os.path.relpath(src_path, self.folder_path))

        # ignore
        self._ignore = False
        if event.is_directory and event.event_type == "modified":
            self._ignore = True
        if self._rel_path in self._single_ignore_paths.keys():
            ignore = self._single_ignore_paths[self._rel_path]
            if not ignore[1]:  # not changed
                self._single_ignore_paths[self._rel_path] = (datetime.datetime.now(), False)
                self._ignore = True
            else:
                enter_time = self._single_ignore_paths[self._rel_path][0]
                if datetime.datetime.now() - enter_time < datetime.timedelta(seconds=0.5):
                    self._ignore = True
                else:
                    self._single_ignore_paths.pop(self._rel_path)

    def on_created(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, file_changes_json.CHANGE_CREATED,
                                           file_changes_json.ACTION_PULL, is_directory=self._is_dir)

    def on_deleted(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, file_changes_json.CHANGE_DELETED,
                                           file_changes_json.ACTION_DELETE, is_directory=self._is_dir)

    def on_modified(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, file_changes_json.CHANGE_MODIFIED,
                                           file_changes_json.ACTION_PULL, is_directory=self._is_dir)

    def on_moved(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, file_changes_json.CHANGE_MOVED,
                                           file_changes_json.ACTION_MOVE, is_directory=self._is_dir)

    def add_single_ignores(self, rel_ignore_paths: List[NormalizedPath]):
        """Single ignores are listed, to be ignored once to be ignored when an event on them occurs.
        Tis is to make copies from the server possible. If changes to the ignored file/folder happens in a short
        time (0.5s) both changes are ignored. This is because a copy is tracked as create and then on modify."""
        self._single_ignore_paths.update({path: (datetime.datetime.now(), False) for path in rel_ignore_paths})
