Threads
=======

Client
-------

::

    MainThread
        |
        |
        | ___________ Thread-N (tray.icon.run)
        |               (runs main.py code)
        |                       |
        |                       |
    tray.mainloop()             |
                                |--------------------- i * Thread-M (Folder watch. for i folders watching)
                                |--------------------- Thread-Q (Watchdog BaseObserver??)
                                |
                                |
                                |--------------------- ServerCommunicator
                                |                           |
                                |                   communicator.connect()
                        connector.try_connect()             *
                                *                           |
                                |                       stop or wait_for_new_input
                                |                           |
                                |
                            GUI.main()
                                *
                                *
