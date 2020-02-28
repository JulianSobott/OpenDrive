Tests
========

Every module should have a separate test module. The test module has the name, prepended with ``test_``.
e.g. ``authentication.py`` and ``test_authentication.py``. All test modules are located in the test package, where
they are located in the real project (server_side, client_side, general).

In tests often a special setup is needed. Because some setups are needed in multiple different modules, the setups
may be written as separate helper functions. These helper functions may be located in the test file or in separate
modules. A helper function should be located in a higher level, the more general it is and the more often it is used.

Helper functions are prepended with ``h_`` to signal, that this is not executed in the real program, but only in tests.

Network vs normal tests
-----------------------

Some functions call functions over the network. For them a server/client process needs to be running.

Rules
*****

- functions that would make a call over the network are always mocked. The other side implementation is out of scope
- functions that are called over the network can be mocked depending on the config
