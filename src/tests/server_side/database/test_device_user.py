import unittest
import uuid
import secrets

from OpenDrive.server_side import database, paths
from OpenDrive.general.database import delete_db_file
from tests.od_logging import logger
from tests.server_side.database.test_devices import TestDatabaseDevices
from tests.server_side.database.test_users import TestDatabaseUsers


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
        device = TestDatabaseDevices.helper_create_dummy_device()
        user = TestDatabaseUsers.helper_create_dummy_user()
        database.DeviceUser.create(device.id, user.id)
        device_user = database.DeviceUser.get_by_ids(device.id, user.id)
        self.assertEqual(device_user.device_id, device.id)
        self.assertEqual(device_user.user_id, user.id)


if __name__ == '__main__':
    unittest.main()
