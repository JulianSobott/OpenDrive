import datetime
import unittest
import uuid
import secrets

from server_side import database, paths, authentication
from general.database import delete_db_file
from server_side.database import Token
from src.tests.od_logging import logger


class TestRegistration(unittest.TestCase):

    def setUp(self):
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()

    def test_add_update_device_new(self):
        mac = str(uuid.getnode())
        authentication._add_update_device(mac)
        all_devices = database.Device.get_all()
        self.assertEqual(1, len(all_devices))
        self.assertEqual(mac, all_devices[0].mac_address)

    def test_add_update_device_expires(self):
        pass

    def test_add_update_device_existing(self):
        pass

    def test_register_user_device(self):
        username = "Anne"
        password = "2hj:_sAdf"
        email = None
        mac = str(uuid.getnode())
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, Token)
        all_devices = database.Device.get_all()
        self.assertEqual(1, len(all_devices))
        all_users = database.User.get_all()
        self.assertEqual(1, len(all_users))
        user = all_users[0]
        self.assertEqual(user, database.User(1, username, user.password, email))


if __name__ == '__main__':
    unittest.main()
