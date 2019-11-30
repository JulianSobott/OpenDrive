"""
:module: OpenDrive.client_side.file_changes
:synopsis: Tracks changes to files in all defined folders.
:author: Julian Sobott

public functions
----------------

.. autofunction:: add_folder
.. autofunction:: add_single_ignores
.. autofunction:: remove_folder_from_watching
.. autofunction:: remove_single_ignore
.. autofunction:: start_observing
.. autofunction:: stop_observing

public members
------------------

.. autodata:: sync_waiter
    :annotation: = Singleton of the SyncWaiter

private functions
-----------------

.. autofunction:: _add_watcher
.. autofunction:: _get_event_handler
.. autofunction:: _remove_watcher

private classes
---------------

.. autoclass:: FileSystemEventHandler
    :members:
    :show-inheritance:

.. autoclass:: SyncWaiter

"""
import os
from typing import List, Dict, Tuple, Optional
from watchdog import events as watchdog_events, observers as watchdog_observers
from watchdog.observers.api import ObservedWatch
import datetime
import threading

from OpenDrive.client_side.od_logging import logger_sync
from OpenDrive.client_side import paths, file_changes_json
from OpenDrive.general import file_changes_json as gen_json

from OpenDrive.general.paths import normalize_path, NormalizedPath


observer = watchdog_observers.Observer()
watchers: Dict[NormalizedPath, Tuple['FileSystemEventHandler', ObservedWatch]] = {}


def start_observing() -> None:
    """Start watching at all folders in a new thread. Calling this is enough and no further function calls inside this
    module are needed."""
    file_changes_json.init_file()
    all_folders = file_changes_json.get_all_data()
    logger_sync.info(f"Watching at folders for changes: {all_folders}")
    for folder_path, folder in all_folders.items():
        _add_watcher(folder_path, folder["include_regexes"], folder["exclude_regexes"])
    observer.start()


def stop_observing():
    """Protects the `observer` from external access"""
    global watchers
    global observer
    observer.stop()
    observer.join()
    watchers = {}
    observer.__init__()


def add_folder(abs_folder_path: str, include_regexes: List[str] = (".*",),
               exclude_regexes: List[str] = (), remote_name: Optional[str] = None) -> bool:
    """If possible add folder to file and start watching. Returns True, if the folder was added."""
    assert isinstance(include_regexes, list) or isinstance(include_regexes, tuple)
    assert isinstance(exclude_regexes, list) or isinstance(exclude_regexes, tuple)
    abs_folder_path = normalize_path(abs_folder_path)
    added = file_changes_json.add_folder(abs_folder_path, include_regexes, exclude_regexes, remote_name)
    if not added:
        return False
    _add_watcher(abs_folder_path, include_regexes, exclude_regexes)
    logger_sync.info(f"Start watching at new folder: {abs_folder_path}, include_regexes={include_regexes}, "
                     f"exclude_regexes={exclude_regexes}")
    return True


def remove_folder_from_watching(abs_folder_path: str) -> None:
    """Stops watching at the folder and removes it permanently from the json file"""
    norm_folder_path = normalize_path(abs_folder_path)
    _remove_watcher(norm_folder_path)
    file_changes_json.remove_folder(norm_folder_path)
    logger_sync.info(f"Stop watching at folder: {abs_folder_path}")


def add_single_ignores(abs_folder_path: str, rel_paths: List[NormalizedPath]) -> None:
    """Add folder and file names that shall be ignored, because they are pulled from the server."""
    event_handler = _get_event_handler(normalize_path(abs_folder_path))
    event_handler.add_single_ignores(rel_paths)


def remove_single_ignore(abs_folder_path: str, rel_paths: str) -> None:
    """This must be called, when the file is finished with copying"""
    event_handler = _get_event_handler(normalize_path(abs_folder_path))
    event_handler.remove_single_ignores(normalize_path(rel_paths))


def _add_watcher(abs_folder_path: NormalizedPath, include_regexes: List[str] = (".*",),
                 exclude_regexes: List[str] = ()):
    """Watcher, that handles changes to the specified folder."""
    event_handler = FileSystemEventHandler(abs_folder_path, include_regexes, exclude_regexes)
    watch = observer.schedule(event_handler, abs_folder_path, recursive=True)
    watchers[abs_folder_path] = event_handler, watch


def _remove_watcher(abs_folder_path: NormalizedPath):
    """Stops watching"""
    event_handler, watch = watchers.pop(abs_folder_path)
    observer.remove_handler_for_watch(event_handler, watch)
    observer.unschedule(watch)


def _get_event_handler(abs_folder_path: NormalizedPath) -> 'FileSystemEventHandler':
    norm_folder_path = abs_folder_path
    assert norm_folder_path in watchers.keys(), f"No event_handler, watches at the specified folder: {norm_folder_path}"
    event_handler, _ = watchers[norm_folder_path]
    return event_handler


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
        """Known issue with watchdog: When a directory is deleted, it is dispatched as FileDeleteEvent. Because after it
        is deleted it is not possible to check whether it was a directory or a file. So when handling a remove
        change, it can be both a file or a directory.
        """
        # Metadata
        self._is_dir = event.is_directory
        src_path = event.src_path
        self._rel_path = normalize_path(os.path.relpath(src_path, self.folder_path))

        # ignore
        self._ignore = False
        if event.is_directory and event.event_type == "modified":
            # Only meta data of the directory is modified. This data is not tracked
            self._ignore = True
        if self._rel_path in self._single_ignore_paths.keys():
            ignore = self._single_ignore_paths[self._rel_path]
            if not ignore[1]:  # not changed
                self._single_ignore_paths[self._rel_path] = (datetime.datetime.now(), True)
                self._ignore = True
            else:
                enter_time = self._single_ignore_paths[self._rel_path][0]
                if datetime.datetime.now() - enter_time < datetime.timedelta(seconds=0.1):
                    self._ignore = True
                else:
                    self._single_ignore_paths.pop(self._rel_path)
        if not self._ignore:
            sync_waiter.sync()
            logger_sync.debug(f"{event.event_type}: {os.path.relpath(event.src_path, self.folder_path)}")

    def on_created(self, event):
        if self._ignore:
            return
        if self._is_dir:
            action = gen_json.ACTION_MKDIR
        else:
            action = gen_json.ACTION_PULL
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, action, is_directory=self._is_dir)

    def on_deleted(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, gen_json.ACTION_DELETE,
                                           is_directory=self._is_dir)

    def on_modified(self, event):
        if self._ignore:
            return
        file_changes_json.add_change_entry(self.folder_path, self._rel_path, gen_json.ACTION_PULL,
                                           is_directory=self._is_dir)

    def on_moved(self, event):
        if self._ignore:
            return
        old_file_path = self._rel_path
        new_file_path = paths.normalize_path(os.path.relpath(event.dest_path, self.folder_path))
        file_changes_json.add_change_entry(self.folder_path, old_file_path, gen_json.ACTION_MOVE,
                                           is_directory=self._is_dir, new_file_path=new_file_path)

    def add_single_ignores(self, rel_ignore_paths: List[NormalizedPath]):
        """Single ignores are listed, to be ignored once to be ignored when an event on them occurs.
        This is to make copies from the server possible. This MUST be removed, after the file is finished creating."""
        self._single_ignore_paths.update({path: (datetime.datetime.now(), False) for path in rel_ignore_paths})

    def remove_single_ignores(self, rel_ignore_path: NormalizedPath):
        """This must be called, when the file is finished with copying"""
        assert rel_ignore_path in self._single_ignore_paths.keys(), "Can't remove file from ignoring, that was never " \
                                                                    f"added. {self.folder_path}/{rel_ignore_path}"
        self._single_ignore_paths.pop(rel_ignore_path)


class SyncWaiter:
    """Provides a waiter that sleeps until a synchronization happens. This waiter may be used in other modules,
    that rely on be notified if a change happens."""

    def __init__(self):
        self.waiter = threading.Event()

    def sync(self):
        """Call this, when a synchronization between server and client is wanted."""
        self.waiter.set()


sync_waiter = SyncWaiter()
