TODOs
======

✓

- GUI
    - config synchronization
      - detect every file extension in folders and make selectable
      - exclude folders
        - Add new folder when picking server folder
    - asynchronous server calls
- tests
    - each function at least one test
    - random tests for api functions
    - network: option for fast and full tests
        - fast: more functions are mocked
- Make all threads controllable
- difficult cases handling
    - connection loss
    - file changes while synchronization
- performance improvement
    - only synchronize file changes
    - multiple socket connections?
    - move expensive functions to C++?
- Web server
- installation
    - easy and fast to setup