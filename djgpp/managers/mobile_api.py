# built-in
import json

# app
from .base import WebBase


URL = 'https://play.google.com/store/xhr/getdoc?authuser=0'


class MobileAPI(WebBase):
    def download(self, app_id, language='en'):
        """Get and extract permissions from server.
        """
        response = self.api.post(
            URL,
            data=dict(
                ids=app_id,
                hl=language,
                xhr=1,
            ),
        )
        # strip junk from response body begining and decode
        data = json.loads(response.text.split('\n', 1)[-1])
        # get only permissions lists
        data = list(data[0][2].values())[0]
        data = data[0][2][0][65]['42656262'][1]
        return self.extract(data)

    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            return []

        strs = [element for element in content if isinstance(element, str)]
        if strs:
            return [strs]

        result = []
        for element in content:
            result.extend(cls.extract(element))
        return result

    def translate(self, objects, language, commit=True):
        return objects
