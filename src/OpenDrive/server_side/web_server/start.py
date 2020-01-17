"""
:module: OpenDrive.server_side.web_server.start
:synopsis: Web server that makes files accessible over the browser
:author: Julian Sobott

public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
from OpenDrive.server_side.od_logging import init_logging

from flask import Flask, render_template
import os

from OpenDrive.server_side.web_server.explorer import build_explorer


init_logging()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/explorer")
def explorer():
    return build_explorer()


if __name__ == '__main__':
    app.run()
