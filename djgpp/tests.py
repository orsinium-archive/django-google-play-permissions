# django
from django.test import TestCase

# app
from .controllers import PermissionController


class TestController(TestCase):
    def setUp(self):
        self.controller = PermissionController()
