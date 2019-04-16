File exchanges
================

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