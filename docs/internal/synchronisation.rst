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

Start up
---------

Client starts and want to synchronise with the server. Also client was offline and is online again.

- Same as normal case

First init
-----------

A new folder is added to synchronise. Both client and server folders may have content already.

- Define what to do with non existing/different files at both sides

    - Copy
    - Delete

- Interchange files
- Start with normal procedure


General procedure
------------------

On any change at the client side the server should be notified and a synchronization process should start.
Therefore a connection between server and client is necessary. The connection starts, when the client starts
and is online. A mechanism to test if it is only or in other words, if it *can connect to the server* is necessary.
How to connect: the device needs to identify itself and authenticate, that it is allowed to connect to the server.
There are several ways to achieve this. The user can choose which he/she want to choose.

1. The user has to enter his/her credentials

    - Necessary when the following fails
    - Not very user friendly
    - Very secure

2. Auto-login - login is stored in a file

    - The device logs in with multiple data, that is unique per device
    - Should be also very secure, but there are ways to crack?
    - Very user friendly
    - Default case

To login the user needs an existing account for auto login the device must be registered.
At manual login the the device may be registered (depends on the users choice). To create
an account the user needs to register.