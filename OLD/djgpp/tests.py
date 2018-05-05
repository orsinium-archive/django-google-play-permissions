# django
from django.test import TestCase

# app
from .management.commands.retrieve_permissions import Command
from .managers.android_api import AndroidAPI
from .managers.web_api import WebAPI
from .managers.mobile_api import MobileAPI
from .managers.web_interface import WebInterface


class TestPermissionsRetrieve(TestCase):
    def test_groups_creation(self):
        groups = Command.create_groups()
        names = [group.text for group in groups]
        self.assertIn('Other', names)
        self.assertIn('Camera', names)
        self.assertIn('SMS', names)

    def test_create_permissions(self):
        Command.create_groups()
        permissions = Command.create_permissions()
        # check names
        names = [permission.text for permission in permissions]
        self.assertIn('Battery stats', names)
        self.assertIn('Broadcast SMS', names)

        # check parents
        for permission in permissions:
            if permission.text == 'Broadcast SMS':
                self.assertEqual(permission.parent.text, 'SMS')
                break
        else:
            self.assertTrue(False)  # permission not found


class TestAndroidAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        Command.create_groups()
        Command.create_permissions()
        return super(TestAndroidAPI, cls).setUpClass()

    def setUp(self):
        self.manager = AndroidAPI()

    def test_download(self):
        permissions = self.manager.download('org.telegram.messenger')
        self.assertIn('android.permission.ACCESS_COARSE_LOCATION', permissions)
        self.assertIn('com.oppo.launcher.permission.READ_SETTINGS', permissions)

    def test_parse(self):
        data = self.manager.download('org.telegram.messenger')
        permissions = self.manager.parse(data)
        names = [permission.text for permission in permissions]
        self.assertIn('Wake lock', names)
        self.assertIn('Receive SMS', names)

        # check parents
        for permission in permissions:
            if permission.text == 'Receive SMS':
                self.assertEqual(permission.parent.text, 'SMS')
                break
        else:
            self.assertTrue(False)  # permission not found


class TestWebInterface(TestCase):
    def setUp(self):
        self.manager = WebInterface()

    def test_download(self):
        permissions = self.manager.download('org.telegram.messenger')
        block = (
            'Identity',
            [
                'find accounts on the device',
                'add or remove accounts',
                'read your own contact card',
            ],
        )
        self.assertIn(block, permissions)

    def test_parse(self):
        data = self.manager.download('org.telegram.messenger')
        permissions = self.manager.parse(data)
        names = [permission.text for permission in permissions]
        self.assertIn('Receive text messages (SMS)', names)

        # check parents
        for permission in permissions:
            if permission.text == 'Receive text messages (SMS)':
                self.assertEqual(permission.parent.text, 'SMS')
                break
        else:
            self.assertTrue(False)  # permission not found


class TestWebAPI(TestCase):
    def setUp(self):
        self.manager = WebAPI()

    def test_download(self):
        permissions = self.manager.download('org.telegram.messenger')
        block = (
            'Contacts',
            [
                'find accounts on the device',
                'read your contacts',
                'modify your contacts',
            ],
        )
        self.assertIn(block, permissions)

    def test_parse(self):
        data = self.manager.download('org.telegram.messenger')
        permissions = self.manager.parse(data)
        names = [permission.text for permission in permissions]
        self.assertIn('Receive text messages (SMS)', names)

        # check parents
        for permission in permissions:
            if permission.text == 'Receive text messages (SMS)':
                self.assertEqual(permission.parent.text, 'SMS')
                break
        else:
            self.assertTrue(False)  # permission not found


class TestMobileAPI(TestCase):
    def setUp(self):
        self.manager = MobileAPI()

    def test_download(self):
        permissions = self.manager.download('org.telegram.messenger')
        block = [
            'add or remove accounts',
            ('Allows the app to perform operations like adding and removing accounts, '
             'and deleting their password.'),
        ]
        self.assertIn(block, permissions)

    def test_parse(self):
        data = self.manager.download('org.telegram.messenger')
        permissions = self.manager.parse(data)
        names = [permission.text for permission in permissions]
        self.assertIn('Receive text messages (SMS)', names)