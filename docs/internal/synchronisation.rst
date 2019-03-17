Synchronisation
=================


On this site the process of synchronisation is described. All kinds of authentications are ignored and are seen
as given.

Normal case
------------

Everything is running for a while. No setup/init stuff and no border cases.

#. Client start synchronisation in a given interval (only when something changed at server or client)
#. Client sends db file to server
#. Client removes all changes from db
#. Server computes al files to interchange

    #. Get the device_user of current sync
    #. Get all client folders that shall be synced
    #. Merge client_changes with server_changes (client_user)

        #. Merge conflicts?

    #. Server removes all changes from server_changes db (client_user)

#. Server send files
#. Server pull files