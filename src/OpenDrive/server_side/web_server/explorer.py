"""
:module: OpenDrive.server_side.web_server.explorer
:synopsis: Explorer view in the browser
:author: Julian Sobott

public classes
---------------

.. autoclass:: File
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
import os
from collections import namedtuple
from dataclasses import dataclass

from flask import render_template

from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side.od_logging import logger_web


@dataclass
class File:
    name: str
    path: str
    extension: str
    create_date: str


def build_explorer():
    explorer_data = build_content(".")
    return render_template("explorer/explorer.html", explorer_data=explorer_data)


def build_content(path: str):
    abs_path = server_paths.normalize_path(server_paths.FOLDERS_ROOT, path)
    logger_web.debug(abs_path)
    files = os.listdir(abs_path)
    logger_web.debug(files)
    files_content = [File(f, server_paths.normalize_path(path, f), "TODO", "TODO") for f in files]
    Content = namedtuple("Content", "files ")
    content = Content(files_content)
    return content
