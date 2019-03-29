import unittest
import uuid
import secrets

from server_side import database, paths
from general.database import delete_db_file
from src.tests.od_logging import logger


class TestDataBaseDeviceUser(unittest.TestCase):
    def setUp(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()

    @staticmethod
    def helper_create_dummy_device_user():
        pass

    def test_columns(self):
        with database.DBConnection(paths.SERVER_DB_PATH) as db:
            res = db.get("PRAGMA table_info(device_user)")
            table_names = [col[1] for col in res]
            expected = ["device_id", "user_id"]
            self.assertEqual(table_names, expected, "Column names changes")

    def test_create_non_existing(self):
        mac_address = str(uuid.getnode())
        token = secrets.token_hex(32)
        device_id = database.Device.create(mac_address, token)
        device = database.Device.from_id(device_id)
        self.assertEqual(device.mac_address, mac_address)
        self.assertEqual(device.token, token)


if __name__ == '__main__':
    unittest.main()
