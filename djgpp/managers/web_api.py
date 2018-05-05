# built-in
import json

# external
import requests

# app
from ..models import Permission
from ..utils import requests_retry_session
from .base import Base


TEMPLATE = '[[[163726509,[{"163726509":[[null,["$",7],[]]]}],null,null,0]]]'
URL = 'https://play.google.com/_/PlayStoreUi/data'


class WebAPI(Base):
    def connect(self, **credentials):
        self.api = requests_retry_session()

    def download(self, app_id):
        response = self.api.post(
            URL,
            params={'hl': 'en'},
            data={'f.req': TEMPLATE.replace('$', app_id)},
        )
        # strip junk from response body begining and decode
        data = json.loads(response.text.split('\n', 1)[-1])
        # get only permissions lists
        data = list(data[0][2].values())[0]
        # concat permissions without group to "Other" group
        data[1][-1][-1].extend(data[-1])
        # get permissions
        result = []
        for group, _info, permissions in (data[0] + data[1])[1:]:
            result.append((group, [p[-1] for p in permissions]))
        return result

    def parse(self, data):
        objects = []
        for group, permissions in data:
            for name in permissions:
                objects.append(self.get_object(name, group))
        return objects

    def get_object(self, name, group_name):
        parent, _created = Permission.objects.get_or_create(
            text=self.format_name(group_name),
            parent=None,
        )
        obj, _created = Permission.objects.get_or_create(
            text=self.format_name(name),
            defaults=dict(parent=parent),
        )
        return obj

    def format_name(self, name):
        return name[0].upper() + name[1:]
