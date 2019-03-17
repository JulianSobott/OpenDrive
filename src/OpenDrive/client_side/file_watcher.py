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
from OpenDrive.client_side import database, paths
from OpenDrive.general.paths import normalize_path

observer = watchdog_observers.Observer()
watchers: Dict[int, Tuple['FileSystemEventHandler', ObservedWatch]] = {}

__all__ = ["start"]


def start() -> None:
    """Start watching at all folders in a new thread. Calling this is enough and no further function calls inside this
    module are needed."""
    all_folders = database.SyncFolder.get_all()
    for folder in all_folders:
        ignores = database.Ignore.get_by_folder(folder.id)
        patterns = [ignore.pattern for ignore in ignores]
        add_watcher(folder.abs_path, patterns, folder.id)
    observer.start()


def add_folder(abs_folder_path: str, ignore_patterns: List[str] = ()) -> None:
    """Check is folder possible, insert in DB, start watching"""
    abs_folder_path = normalize_path(abs_folder_path)
    can_added = _exist_folder(abs_folder_path)
    if not can_added:
        logger.info(f"Folder {abs_folder_path} can not be added, because it dont exist!")
        return  # TODO: Notify user
    folder_id = _add_folder_to_db(abs_folder_path)
    add_watcher(abs_folder_path, ignore_patterns, folder_id)


def remove_folder_from_watching(abs_folder_path: str = None, folder_id: int = None) -> None:
    """Stops watching at the folder and removes it permanently from the db"""
    assert abs_folder_path is not None or folder_id is not None, "One of both arguments must be not None."
    if folder_id is None:
        folder_id = database.SyncFolder.from_path(abs_folder_path)
    _remove_watcher(folder_id)
    database.SyncFolder.remove_entry(folder_id)


def add_single_ignores(folder_id: int, rel_paths: List[str]) -> None:
    """Add folder and file names that shall be ignored, because they are pulled from the server."""
    assert folder_id in watchers.keys(), f"No event_handler, watches at the specified folder with id {folder_id}"
    event_handler, _ = watchers[folder_id]
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
        sql = f"DELETE FROM ignores WHERE folder_id = ? and pattern in ({','.join(['?']*len(ignores))})"
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


def add_watcher(abs_folder_path: str, ignore_patterns: List[str] = (), folder_id: int = None):
    """Watcher, that handles changes to the specified folder.
    `ignore_patterns` is a ist of all patterns to ignore in regex style."""
    if folder_id is None:
        sync_folder = database.SyncFolder.from_path(abs_folder_path)
        folder_id = sync_folder.id
    event_handler = FileSystemEventHandler(abs_folder_path, folder_id, ignore_patterns)
    watch = observer.schedule(event_handler, abs_folder_path, recursive=True)
    watchers[folder_id] = event_handler, watch


def _remove_watcher(folder_id: int):
    """Stops watching"""
    event_handler, watch = watchers.pop(folder_id)
    observer.remove_handler_for_watch(event_handler, watch)
    observer.unschedule(watch)


class FileSystemEventHandler(watchdog_events.RegexMatchingEventHandler):
    """Track changes inside a folder. Every change will either create a new entry in the `changes` table or change
    an existing one, if no ignore pattern matches."""
    def __init__(self, abs_folder_path: str, folder_id: int, ignore_patterns: List[str] = ()):
        super().__init__(ignore_regexes=ignore_patterns, case_sensitive=False)
        self.folder_path = abs_folder_path
        self._single_ignore_paths: Dict[str, Tuple[datetime.datetime, bool]] = {}
        self._folder_id: int = folder_id
        self._is_dir: bool = False
        self._rel_path: str = ""
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
        self._rel_path = os.path.relpath(src_path, self.folder_path)

        # ignore
        self._ignore = False
        if self._rel_path in self._single_ignore_paths.keys():
            ignore = self._single_ignore_paths[self._rel_path]
            if not ignore[1]:   # not changed
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
        try:
            database.Change.create(self._folder_id, self._rel_path, is_folder=self._is_dir, is_created=True)
        except database.UniqueError:
            pass  # Added file twice. See issue at :func:`on_any_event`

    def on_deleted(self, event):
        if self._ignore:
            return
        database.Change.create(self._folder_id, self._rel_path, is_folder=self._is_dir, is_deleted=True,
                               necessary_action=database.Change.ACTION_DELETE)

    def on_modified(self, event):
        if self._ignore:
            return
        try:
            database.Change.create(self._folder_id, self._rel_path, is_folder=self._is_dir, is_modified=True,
                                   necessary_action=database.Change.ACTION_PULL)
        except database.UniqueError:
            change = database.Change.get_possible_entry(self._folder_id, self._rel_path)
            change.is_modified = True
            change.last_change_time_stamp = change.get_current_time()

    def on_moved(self, event):
        if self._ignore:
            return
        possible_change = database.Change.get_possible_entry(self._folder_id, self._rel_path)
        action = database.Change.ACTION_MOVE
        old_abs_path = event.src_path
        current_rel_path = os.path.relpath(event.dest_path, self.folder_path)
        try:
            pull = possible_change.is_modified or possible_change.is_created
            if pull:
                action = database.Change.ACTION_PULL_DELETE
        except AttributeError:
            pass
        try:
            database.Change.create(self._folder_id, current_rel_path, is_folder=self._is_dir, is_moved=True,
                                   necessary_action=action, old_abs_path=old_abs_path)
        except database.UniqueError:
            change = database.Change.get_possible_entry(self._folder_id, self._rel_path)
            change.is_moved = True
            change.old_abs_path = old_abs_path
            change.current_rel_path = current_rel_path
            change.last_change_time_stamp = change.get_current_time()

    def add_single_ignores(self, rel_ignore_paths: List[str]):
        """Single ignores are listed, to be ignored once to be ignored when an event on them occurs.
        Tis is to make copies from the server possible. If changes to the ignored file/folder happens in a short
        time (0.5s) both changes are ignored. This is because a copy is tracked as create and then on modify."""
        self._single_ignore_paths.update({path: (datetime.datetime.now(), False) for path in rel_ignore_paths})
