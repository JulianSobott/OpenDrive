Databases at the server
=======================

- Filesystem
- user


Filesystem
----------

- file
    - id
    - name
    - path
    - parent
    - owner
    - accesses: list
        - pull, update, create
        - date
        - device
        - user
    - permissions: list
        - user/link
        - permission: read, full
        - expires

- directory
    - id
    - name
    - files: list
    - owner
