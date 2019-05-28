"""
:module: OpenDrive.general.merge_folders
:synopsis: Merge content (files and folders) of two folders. so that both end up identical
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: generate_content_of_folder

private functions
-----------------

.. autofunction:: walk_directories
.. autofunction:: _recursive_generate_content_of_folder


"""
import os

from general.paths import NormalizedPath, normalize_path


def generate_content_of_folder(abs_folder_path: str, only_files_list=False, top_folder_name: str = "") -> dict:
    """
    :param abs_folder_path:
    :param top_folder_name: optional name of the root folder. Used to allow relative path at server
    :param only_files_list: True: Files are only stored as list with only the names. Else: see return
    :return: dict with following structure

        Folder:
            "folder_name": top_folder_name,
            "files": List[Dict["filename": str, "modified_timestamp": str]
            "folders": List[Folder]
    """
    if not os.path.exists(abs_folder_path):
        raise FileNotFoundError
    top_folder_name = top_folder_name if top_folder_name else abs_folder_path
    return _recursive_generate_content_of_folder(abs_folder_path, top_folder_name, only_files_list)


def walk_directories(dir_content: dict, parent_path: NormalizedPath):
    """Directory tree generator.

    For each directory in the directory tree, yields a 3-tuple

        parent_path, dir_path, files (Tuple[filename, timestamp])

        path of file: parent_path + dir_path + file_name
    """
    folder_name = dir_content["folder_name"]
    files = [(f["file_name"], f["modified_timestamp"]) for f in dir_content["files"]]
    yield parent_path, folder_name, files

    for folder in dir_content["folders"]:
        yield from walk_directories(folder, normalize_path(parent_path, dir_content["folder_name"]))


def _recursive_generate_content_of_folder(abs_folder_path: str, folder_name: str, only_files_list):
    content = {
        "folder_name": folder_name,
        "files": [],
        "folders": []
    }
    _, dir_list, file_list = next(os.walk(abs_folder_path))
    for file in file_list:
        file_path = os.path.join(abs_folder_path, file)
        if not only_files_list:
            content["files"].append({"file_name": file, "modified_timestamp": os.path.getmtime(file_path)})
        else:
            content["files"].append(file)
    for dir_name in dir_list:
        abs_path = os.path.join(abs_folder_path, dir_name)
        content["folders"].append(_recursive_generate_content_of_folder(abs_path, dir_name, only_files_list))
    return content
