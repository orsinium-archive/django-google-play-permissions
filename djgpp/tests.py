from django.test import TestCase
from .management.commands.retrieve_permissions import Command


class TestPermissionsRetrieve(TestCase):
    def test_groups_creation(self):
        groups = Command.create_groups()
        names = [group.text for group in groups]
        self.assertIn('Other', names)
        self.assertIn('Camera', names)
        self.assertIn('SMS', names)
