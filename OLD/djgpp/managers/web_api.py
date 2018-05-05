# built-in
import json

# app
from .base import WebBase


TEMPLATE = '[[[163726509,[{"163726509":[[null,["$",7],[]]]}],null,null,0]]]'
URL = 'https://play.google.com/_/PlayStoreUi/data'


class WebAPI(WebBase):
    def download(self, app_id):
        """Get and extract permissions from server.
        """
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
