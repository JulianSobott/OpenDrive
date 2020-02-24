Problem Analysis
----------------

There are following problems (sorted after priority):

- **Threading:**
    - which threads runs when
    - what does each thread do
    - which threads are dependent from another
    - does any thread block the application

- Server opens GUI although it was opened by client

- **Stable run:**
    - Make common procedures stable
        - e.g. connect, disconnect, synchronize, close application
    - Make special cases stable
        - losing connection, file edit while sync, close app while sync

- **Independent modules:**
    - Server independent of client -> Do not import kivy at server
    - install only server/client

- **Sync conflicts**
- **Start on system start**
- **Security**
- **Performance**
    - maybe only transmit changes instead of whole file
- **Installation**
- **External Access**
