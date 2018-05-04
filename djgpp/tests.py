from django.test import TestCase
from .management.commands.retrieve_permissions import Command
from .managers.android_api import AndroidAPI


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
        ...
