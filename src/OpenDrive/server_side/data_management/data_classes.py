"""
:module: OpenDrive.
:synopsis: 
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
from dataclasses import dataclass
from typing import NewType, List, Dict

UID = str
User = int
Device = int
Date = str


@dataclass
class File:
    uid: UID
    name: str
    path: str
    parent: UID
    owner: 'User'
    accesses: List['Access']
    permissions: Dict[User, 'Permission']


@dataclass
class Folder:
    file_node: File
    files: List[File]
    files_not_listed: bool = False


AccessType = NewType("AccessType", str)
PULL = AccessType("pull")
UPDATE = AccessType("update")
CREATE = AccessType("create")
DELETE = AccessType("delete")


@dataclass
class Access:
    type: AccessType
    date: Date
    device: Device
    user: User


PermissionType = NewType("PermissionType", int)
READ = PermissionType(4)
WRITE = PermissionType(2)
EXECUTE = PermissionType(1)


@dataclass
class Permission:
    permissions: PermissionType
    created: Date
    expires: Date
