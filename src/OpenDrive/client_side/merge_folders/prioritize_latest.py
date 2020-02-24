"""
:module: OpenDrive.client_side.merge_folders.prioritize_latest
:synopsis: Copies missing files at both sides. If file exists on both sides, the latest modified is taken.
:author: Julian Sobott


public functions
-----------------

.. autofunction:: prioritize_latest

private functions
--------------------

.. autofunction:: _merge_files_latest
.. autofunction:: _merge_folders_latest
.. autofunction:: _prioritize_latest_recursive

"""
from typing import Tuple, List

from OpenDrive.general.file_exchanges import SyncAction
from OpenDrive.general import file_changes_json as gen_json
from OpenDrive.general.paths import normalize_path, NormalizedPath
from OpenDrive.client_side import synchronization as c_syc


NAME = "Prioritize latest"
DESCRIPTION = "Copies missing files at both sides. If file exists on both sides, the latest modified is taken."


def prioritize_latest(folder_1_content: dict, folder_2_content: dict) -> Tuple[List[SyncAction], List[SyncAction]]:
    return _prioritize_latest_recursive(folder_1_content, folder_2_content, folder_1_content["folder_name"],
                                        folder_2_content["folder_name"], normalize_path(""))


method = prioritize_latest


def _prioritize_latest_recursive(folder_1_content: dict, folder_2_content: dict, f1_path: NormalizedPath,
                                 f2_path: NormalizedPath, rel_path: NormalizedPath):
    """Calls itself recursive to reach inner folders."""
    f1_actions = []
    f2_actions = []
    f1_files: list = folder_1_content["files"]
    f2_files: list = folder_2_content["files"]

    new_f1_actions, new_f2_actions = _merge_files_latest(f1_files, f2_files, f1_path, f2_path, rel_path)
    f1_actions += new_f1_actions
    f2_actions += new_f2_actions

    f1_folders: list = folder_1_content["folders"]
    f2_folders: list = folder_2_content["folders"]
    new_f1_actions, new_f2_actions = _merge_folders_latest(f1_folders, f2_folders, f1_path, f2_path, rel_path)
    f1_actions += new_f1_actions
    f2_actions += new_f2_actions

    return f1_actions, f2_actions


def _merge_files_latest(files1: List[dict], files2: List[dict], f1_path: NormalizedPath, f2_path: NormalizedPath,
                        rel_path: NormalizedPath):
    """Create actions based on the files inside the two folders."""
    f1_actions = []
    f2_actions = []
    f2_file_names = [file["file_name"] for file in files2]
    for f1 in files1:
        try:
            idx = f2_file_names.index(f1["file_name"])
            f2 = files2[idx]
            if f1["modified_timestamp"] > f2["modified_timestamp"]:
                take_1 = True
            else:
                take_1 = False
            f2_file_names.pop(idx)
            files2.pop(idx)
        except ValueError:
            take_1 = True
        if take_1:
            f2_actions.append(c_syc.create_action(normalize_path(f2_path), normalize_path(rel_path, f1["file_name"]),
                                                  gen_json.ACTION_PULL, False,
                                                  remote_abs_path=normalize_path(f1_path, rel_path, f1["file_name"])))
        else:
            f1_actions.append(c_syc.create_action(normalize_path(f1_path), normalize_path(rel_path, f1["file_name"]),
                                                  gen_json.ACTION_PULL, False,
                                                  remote_abs_path=normalize_path(f2_path, rel_path, f1["file_name"])))
    files1.clear()
    if len(files2) > 0:
        new_f2_actions, new_f1_actions = _merge_files_latest(files2, files1, f2_path, f1_path, rel_path)
        f1_actions += new_f1_actions
        f2_actions += new_f2_actions
    return f1_actions, f2_actions


def _merge_folders_latest(folders1: List[dict], folders2: List[dict], f1_path: NormalizedPath, f2_path: NormalizedPath,
                          rel_path: NormalizedPath):
    """Create actions based on the folders inside the two folders."""
    f1_actions = []
    f2_actions = []
    f2_folder_names = [folder["folder_name"] for folder in folders2]
    for f1 in folders1:
        try:
            idx = f2_folder_names.index(f1["folder_name"])
            f2 = folders2[idx]
            new_rel_path = normalize_path(rel_path, f1["folder_name"])
            new_f1_actions, new_f2_actions = _prioritize_latest_recursive(f1["files"], f2["files"],
                                                                          f1_path, f2_path, new_rel_path)
            f1_actions += new_f1_actions
            f2_actions += new_f2_actions
            f2_folder_names.pop(idx)
            folders2.pop(idx)
        except ValueError:
            rel_file_path = normalize_path(rel_path, f1["folder_name"])
            remote_abs_path = normalize_path(f1_path, rel_path, f1["folder_name"])
            f2_actions.append(c_syc.create_action(normalize_path(f2_path), rel_file_path, gen_json.ACTION_PULL,
                                                  True, remote_abs_path=remote_abs_path))
    if len(folders2) > 0:
        new_f2_actions, new_f1_actions = _merge_folders_latest(folders2, folders1, f2_path, f1_path, rel_path)
        f1_actions += new_f1_actions
        f2_actions += new_f2_actions
    return f1_actions, f2_actions
