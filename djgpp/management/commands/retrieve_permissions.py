from django.core.management import BaseCommand
from ...constants import GROUPS, NULL_OBJECT_NAME
from ...managers.android_api import AndroidAPI
from ...models import Permission
import requests
import bs4


class Command(BaseCommand):
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
            text=cls.manager.format_name(NULL_OBJECT_NAME),
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
        for element in table.find_all('td')[1::2]:
            Permission.objects.get_or_create(
                text=cls.manager.format_name(element.find('code').text),
                defaults=dict(
                    parent=cls.manager.get_parent(element.find('code').text),
                    description=' '.join(element.find('p').text.split()),
                )
            )

    def handle(self, *args, **options):
        self.create_groups()
        self.create_permissions()
