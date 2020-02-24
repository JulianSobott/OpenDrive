"""
:module: OpenDrive.server_side.web_server.database.documents
:synopsis: Structure of the mongoDB database
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
from mongoengine import Document, StringField, ReferenceField, ListField, EmbeddedDocument, DateTimeField, \
    EmbeddedDocumentField, connect

__all__ = ["File", "User", "Device", "Access"]

connect("OpenDrive")


class Access(EmbeddedDocument):
    type = StringField(regex="pull|update|create", required=True)
    date = DateTimeField(required=True)
    device = ReferenceField('Device', required=True)
    user = ReferenceField('User', required=True)


class File(Document):
    name = StringField(required=True)
    path = StringField(required=True)
    parent = StringField()
    owner = ReferenceField('User')
    accesses = ListField(EmbeddedDocumentField('Access'))


class User(Document):
    name = StringField(required=True)


class Device(Document):
    name = StringField(required=True)
