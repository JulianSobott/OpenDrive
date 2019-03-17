"""
@author: Julian Sobott

@brief: Tools for accessing a sqlite database

@description:

classes:
    - :class:`DBConnection`
    - :class:`TableEntry`

@external_use:

@internal_use:
"""
import sqlite3
from typing import List
import os

from OpenDrive.general.od_logging import logger


UniqueError = sqlite3.IntegrityError


class MetaDBConnection(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if MetaDBConnection._instance is None:
            MetaDBConnection._instance = super(MetaDBConnection, cls).__call__(*args, **kwargs)
        return MetaDBConnection._instance


class DBConnection(metaclass=MetaDBConnection):
    """Interface to a sqlite database. Used as context-manager, to properly open and close the connection"""

    def __init__(self, abs_db_path: str) -> None:
        self.abs_db_path = abs_db_path
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        self._commit_close_on_exit = True
        self.connected = False

    def __enter__(self) -> 'DBConnection':
        """Opens a connection and initializes the `cursor`"""
        if not self.connected:
            self.connection = sqlite3.connect(self.abs_db_path)
            self.cursor = self.connection.cursor()
            self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits changes and closes the `connection`"""
        if self._commit_close_on_exit:
            self.connection.commit()
            self.connection.close()
            self.connected = False

    def commit_and_close(self):
        self._commit_close_on_exit = True
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def pause_commit_and_close(self):
        self._commit_close_on_exit = False

    """Possible actions at the DB"""

    def get(self, sql: str, args: tuple = ()) -> list:
        """SELECT"""
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def create(self, sql: str, args: tuple = ()) -> None:
        """CREATE"""
        self.cursor.execute(sql, args)

    def insert(self, sql: str, args: tuple = ()) -> int:
        """INSERT (raises sqlite3.IntegrityError, when a existing unique field is inserted"""
        try:
            self.cursor.execute(sql, args)
        except sqlite3.IntegrityError as e:
            raise UniqueError()
        return self.cursor.lastrowid

    def update(self, sql: str, args: tuple = ()) -> None:
        """UPDATE"""
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            logger.error(e)
            raise e

    def delete(self, sql: str, args: tuple = ()) -> None:
        """DELETE"""
        self.cursor.execute(sql, args)


class TableEntry(object):
    """Interface between python and DB entry.
        Call a static method :func:`from_...()` to get a object, initialized with the values of the db.
        All class have the static method :func:`from_id(id_)` implemented.
        Call the static method :func:`create(...)` to insert a new entry in the db and get the `id`.
        Call the setter properties, to change the values in the db.
        To get a value from the DB call the getters.
        NOTE: if a value is changed, the :func:`update()` function must be called first, to update all values.

        All subclasses must override the `TABLE_NAME`, `DB_PATH`, `PRIMARY_KEY_NAME` attributes
        and must provide the :func:`create` function.
        """
    TABLE_NAME: str
    DB_PATH: str
    PRIMARY_KEY_NAME: str

    def __init__(self, *args):
        self._id = -1

    @property
    def id(self):
        """PRIMARY_KEY value"""
        return self._id

    def update(self):
        """Get all values from the db and sets them to the object"""
        assert self.PRIMARY_KEY_NAME is not None, "Set PRIMARY_KEY_NAME attribute in subclass"
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE {self.PRIMARY_KEY_NAME} = ?"
        with DBConnection(self.DB_PATH) as db:
            ret = db.get(sql, (self.id,))
        if len(ret) == 0:
            raise KeyError(f"No change entry in 'ignores' with id {self.id}!")
        if len(ret) > 1:
            raise KeyError(f"To many entries in '{self.TABLE_NAME}({self.PRIMARY_KEY_NAME})' with value {self.id}! ")
        self.__init__(*ret[0])
        return self

    @classmethod
    def from_id(cls, id_) -> 'TableEntry':
        """Returns a :class:`TableEntry` object with all values set.
        The values are the one fitting to the primary key id.
        raises a KeyError if not exactly one entry exists"""
        return cls._from_column(cls.PRIMARY_KEY_NAME, id_)

    @classmethod
    def _from_column(cls, column_name: str, value) -> 'TableEntry':
        """Returns a :class:`TableEntry` object with all values set.
                The values are the one fitting to the `column_name` and `value`
                raises a KeyError if not exactly one entry exists"""
        assert cls.DB_PATH is not None, "Set the DB_PATH in the subclass"
        assert cls.TABLE_NAME is not None, "Set the TABLE_NAME in the subclass"
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {column_name} = ?"
        with DBConnection(cls.DB_PATH) as db:
            ret = db.get(sql, (value,))
        if len(ret) == 0:
            raise KeyError(f"No entry in '{cls.TABLE_NAME}({column_name})' with value {value}!")
        if len(ret) > 1:
            raise KeyError(f"To many entries in '{cls.TABLE_NAME}({column_name})' with value {value}! ")
        return cls(*ret[0])

    @classmethod
    def from_columns(cls, where_clause: str, args: tuple) -> List['TableEntry']:
        """Returns a list with initialized objects from the inherited class of :class:`TableEntry`.
        The `where_clause` must be a sqlite like parameterized WHERE clause without the WHERE. e.g. "name = ?".
        The args must be a tuple with all values for the parameterized string."""
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {where_clause}"
        with DBConnection(cls.DB_PATH) as db:
            ret = db.get(sql, args)
        return [cls(*values) for values in ret]

    @classmethod
    def get_all(cls):
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        with DBConnection(cls.DB_PATH) as db:
            ret = db.get(sql, tuple())
        return [cls(*values) for values in ret]

    def _change_field(self, field_name: str, new_value) -> None:
        self._prevent_sql_injection(field_name)
        sql = f'UPDATE "{self.TABLE_NAME}" SET {field_name} = ? WHERE "{self.PRIMARY_KEY_NAME}" = ?'
        with DBConnection(self.DB_PATH) as db:
            db.update(sql, (new_value, self.id))

    @classmethod
    def remove_entry(cls, entry_id: int) -> None:
        sql = f'DELETE FROM {cls.TABLE_NAME} WHERE {cls.PRIMARY_KEY_NAME} = ?'
        with DBConnection(cls.DB_PATH) as db:
            db.delete(sql, (entry_id,))

    @staticmethod
    def _prevent_sql_injection(string: str):
        if ";" in string or ")" in string:
            raise ValueError("Preventing possible sql injection")


def delete_db_file(path):
    try:
        extension = os.path.splitext(path)[1]
        if extension != ".db":
            raise Exception(f"Cannot delete non .db file! {path}")
        os.remove(path)
    except FileNotFoundError:
        logger.debug(f"Could not delete non existing db file. {path}")
        pass

