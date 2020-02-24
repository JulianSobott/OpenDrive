"""
:module: OpenDrive.client_side.gui.explorer.directory_dialog
:synopsis: Dialog for selecting a directory
:author: Julian Sobott

public functions
----------------

.. autofunction:: get_directory_path

"""

import tkinter
from tkinter import filedialog
from pathlib import Path

from OpenDrive.general import paths


def get_directory_path(window_title="OpenDrive: Select a directory") -> paths.NormalizedPath:
    """Opens a platform specific dialog, where the user can select a directory.

    Returns
    -------
    path_to_directory: NormalizedPath
    """
    local_root = tkinter.Tk()
    local_root.withdraw()
    directory = tkinter.filedialog.askdirectory(parent=local_root,
                                                title=window_title,
                                                initialdir=Path.home(),
                                                )
    local_root.destroy()
    return paths.normalize_path(directory)


if __name__ == '__main__':
    d = get_directory_path()
    print(d)
