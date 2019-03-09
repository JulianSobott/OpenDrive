"""
@author: Julian Sobott
@brief: Tools for accessing a sqlite database
@description:

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
        """Opens a connection in initializes the cursor"""
        self.connection = sqlite3.connect(self.abs_db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection"""
        self.connection.close()

    def get(self, sql: str, args: tuple = ()) -> list:
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def create(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def insert(self, sql: str, args: tuple = ()) -> int:
        self.cursor.execute(sql, args)
        return self.cursor.lastrowid

    def update(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)

    def delete(self, sql: str, args: tuple = ()) -> None:
        self.cursor.execute(sql, args)
