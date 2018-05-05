# external
import bs4
import requests

# django
from django.core.management import BaseCommand

# app
from ...constants import GROUPS, NULL_OBJECT_NAME
from ...managers.android_api import AndroidAPI
from ...models import Permission


class Command(BaseCommand):
    """Download and save android apps permissions and groups.
    
    This command get:
    1. groups from constants.
    2. permissions and descriptions from official documentation.
    
    AndroidAPI manager use this data for better results.
    """
    help = 'Download and save android apps permissions and groups'
    manager = AndroidAPI

    @classmethod
    def create_groups(cls):
        groups = []
        # create groups
        for name in GROUPS:
            group, _created = Permission.objects.get_or_create(
                text=cls.manager.format_name(name),
                parent=None,
            )
            groups.append(group)
        # create null group
        group, _created = Permission.objects.get_or_create(
            text=NULL_OBJECT_NAME,
            parent=None,
        )
        groups.append(group)
        return groups

    @classmethod
    def create_permissions(cls):
        # download
        response = requests.get('https://developer.android.com/reference/android/Manifest.permission')
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', id='constants')
        # save
        permissions = []
        null_object = Permission.objects.get(text=NULL_OBJECT_NAME)
        for element in table.find_all('td')[1::2]:
            permission, _created = Permission.objects.get_or_create(
                text=cls.manager.format_name(element.find('code').text),
                defaults=dict(
                    parent=cls.manager.get_parent(element.find('code').text) or null_object,
                    description=' '.join(element.find('p').text.split()),
                )
            )
            permissions.append(permission)
        return permissions

    def handle(self, *args, **options):
        self.create_groups()
        self.create_permissions()