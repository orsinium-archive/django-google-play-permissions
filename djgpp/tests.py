# django
from django.test import TestCase

# app
from .controllers import PermissionController


class TestController(TestCase):
    def setUp(self):
        self.controller = PermissionController()

    def test_get_names(self):
        data = self.controller.get_names('org.telegram.messenger', 'en')
        block = [
            'find accounts on the device',
            ('Allows the app to get the list of accounts known by the device. '
             'This may include any accounts created by applications you have installed.'),
        ]
        self.assertIn(block, data)

        data = self.controller.get_names('org.telegram.messenger', 'ru')
        block = [
            'Поиск аккаунтов на устройстве',
            ('Приложение сможет получить список всех используемых на устройстве аккаунтов, '
             'в том числе созданных установленными приложениями.'),
        ]
        self.assertIn(block, data)

    def test_get_groups(self):
        data = self.controller.get_groups('org.telegram.messenger', 'en')
        self.assertIn('find accounts on the device', data)
        self.assertIn('Contacts', data.values())
        self.assertIn('Other', data.values())

        data = self.controller.get_groups('org.telegram.messenger', 'ru')
        self.assertIn('find accounts on the device', data)
        self.assertIn('Контакты', data.values())
        self.assertIn('Другое', data.values())
