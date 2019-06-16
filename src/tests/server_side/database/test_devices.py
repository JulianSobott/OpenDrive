"""
:module:
:synopsis:
:author: Julian Sobott

"""
import datetime
import unittest
import uuid

from OpenDrive.server_side import database, paths
from OpenDrive.server_side.database import Token
from tests.server_side.database.helper_database import h_setup_server_database


class TestDatabaseDevices(unittest.TestCase):

    def setUp(self):
        h_setup_server_database()

    def test_columns(self):
        with database.DBConnection(paths.SERVER_DB_PATH) as db:
            res = db.get("PRAGMA table_info(devices)")
            table_names = [col[1] for col in res]
            expected = ["device_id", "user_id", "mac_address", "token", "token_expires"]
            self.assertEqual(table_names, expected, "Column names changes")

    def test_create_non_existing(self):
        user_id = 1
        mac_address = str(uuid.getnode())
        token = Token(32)
        token_expires = datetime.datetime(2020, 12, 31)
        device_id = database.Device.create(user_id, mac_address, token, token_expires)
        device = database.Device.from_id(device_id)
        self.assertEqual(device.mac_address, mac_address)
        self.assertEqual(device.token, token)
