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


class DBConnection:
    """Interface to a sqlite database. Used as context-manager, to properly open and close the connection"""

    def __init__(self, abs_db_path: str) -> None:
        self.abs_db_path = abs_db_path
        self.connection: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def __enter__(self) -> 'DBConnection':
        """Opens a connection and initializes the `cursor`"""
        self.connection = sqlite3.connect(self.abs_db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits changes and closes the `connection`"""
        self.connection.commit()
        self.connection.close()

    """Possible actions at the DB"""

    def get(self, sql: str, args: tuple = ()) -> list:
        """SELECT"""
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def create(self, sql: str, args: tuple = ()) -> None:
        """CREATE"""
        self.cursor.execute(sql, args)

    def insert(self, sql: str, args: tuple = ()) -> int:
        """INSERT"""
        self.cursor.execute(sql, args)
        return self.cursor.lastrowid

    def update(self, sql: str, args: tuple = ()) -> None:
        """UPDATE"""
        self.cursor.execute(sql, args)

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

    def _change_field(self, field_name: str, new_value) -> None:
        if ";" in field_name or ")" in field_name:
            raise ValueError("Preventing possible sql injection")
        sql = f'UPDATE "{self.TABLE_NAME}" SET {field_name} = ? WHERE "{self.PRIMARY_KEY_NAME}" = ?'
        with DBConnection(self.DB_PATH) as db:
            db.update(sql, (new_value, self.id))
