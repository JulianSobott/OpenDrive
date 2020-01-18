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
from flask_pymongo import PyMongo

from OpenDrive.server_side import paths as server_paths
from OpenDrive.server_side.od_logging import logger_web
from OpenDrive.server_side.web_server.database import *


def build_explorer(mongo: PyMongo):
    explorer_data = build_content(mongo, ".")
    return render_template("explorer/explorer.html", explorer_data=explorer_data)


def build_content(mongo: PyMongo, path: str):
    abs_path = server_paths.normalize_path(server_paths.FOLDERS_ROOT, path)
    logger_web.debug(abs_path)
    files = os.listdir(abs_path)
    logger_web.debug(files)
    files = [File(name=f, path=server_paths.normalize_path(path, f)) for f in files]
    File.objects.insert(files)
    Content = namedtuple("Content", "files ")
    content = Content(files)
    return content
