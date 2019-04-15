import datetime
import unittest
import uuid
import shutil
from typing import Tuple
import os

from OpenDrive.server_side import database, paths, authentication
from OpenDrive.general.database import delete_db_file
from OpenDrive.server_side.database import Token
from tests.od_logging import logger
from tests.server_side import test_folders


class TestRegistration(unittest.TestCase):

    def setUp(self):
        test_folders.TestFolders.initialize_standard_folders()
        self.static_setup()

    @staticmethod
    def static_setup():
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()
        authentication._set_user_authenticated = lambda user_id: None  # Deactivates the function, that is only
        # available,
        # when a client is connected

    def tearDown(self) -> None:
        pass

    @staticmethod
    def helper_register_dummy_user_device() -> Tuple[database.User, database.Device, Token]:
        copy_set_user_authenticated = authentication._set_user_authenticated
        TestRegistration.static_setup()

        username = "Anne"
        password = "2hj:_sAdf"
        email = None
        mac = str(uuid.getnode())
        token = authentication.register_user_device(username, password, mac, email)
        user = database.User(1, username, password, email)
        device = database.Device.get_by_mac(mac)

        authentication._set_user_authenticated = copy_set_user_authenticated
        return user, device, token

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

    def test_register_user_device_existing(self):
        username = "Anne"
        password = "2hj:_sAdf"
        email = None
        mac = str(uuid.getnode())
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, Token)
        token = authentication.register_user_device(username, password, mac, email)
        self.assertIsInstance(token, str)


class TestLogin(unittest.TestCase):

    def setUp(self):
        test_folders.TestFolders.initialize_standard_folders()
        delete_db_file(paths.SERVER_DB_PATH)
        database.create_database()
        authentication._set_user_authenticated = lambda user_id: None   # Deactivates the function, that is only
        # available,
        # when a client is connected

    def test_login_manual_user_device(self):
        user, device, token = TestRegistration.helper_register_dummy_user_device()
        username = user.username
        password = user.password
        mac = device.mac_address
        token = authentication.login_manual_user_device(username, password, mac)
        self.assertIsInstance(token, Token)

    def test_login_auto(self):
        user, device, token = TestRegistration.helper_register_dummy_user_device()
        mac = device.mac_address
        ret = authentication.login_auto(token, mac)
        self.assertTrue(ret)


if __name__ == '__main__':
    unittest.main()
