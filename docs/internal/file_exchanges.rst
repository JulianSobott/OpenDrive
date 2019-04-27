File exchanges
================

All file exchanges actions happens client side. The client get all changes from the server and merges them with the
local changes. After this is done the server iterates over all actions of the server and calls the appropiate
function at the server (``pull``, ``move``, ``delete``). The client also handles all the necessary actions for the
client. So it iterates over all actions of the client. It calls locally: ``move``, ``delete`` or at the server
``get_file``. ``move`` and ``delete`` may be defined in general. I start with implementation with the simple ones
(move and delete).

The client calls move file: Only possible to move inside users root folder. relative path to users root as argument
is sufficient. server functions then adds the users path and calls the general function. Where to test it: server

Client:
- move
- delete
- get_file # from server


Server:
- move
- delete
- pull_file # from client

A loop at the client side is needed, that loops though all changes and executes the proper functions.


Files between the server and the client are exchanged after all necessary actions are calculated. Actions are
calculated, when there were changes and the server and client merge the changes.

Actions
----------

An action defines, what the device has to do with a specific file. Following actions are available:
- Pull: Pulls the file from the other side and saves it at the proper path. Overwrites exiting.
- Move: Moves the file to the (local) destination. Overwrites exiting.
- Delete: Deletes the file

**Considerations:**
Actions could be a class with only data. Every Action class could execute the proper Action.