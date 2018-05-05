# built-in
import json

# app
from .base import WebBase
from ..models import Permission


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

    def parse(self, data):
        """Convert permissions names list to Permission objects.
        """
        objects = []
        for name, description in data:
            objects.append(self.get_object(name, description))
        return objects

    def get_object(self, name, description):
        """Get or create object by name.
        """
        obj, _created = Permission.objects.get_or_create(
            text=self.format_name(name),
            defaults=dict(description=description),
        )
        return obj

    def translate(self, app_id, objects, language, commit=True):
        """Download translated data and write it into objects.
        """
        data = self.download(app_id, language)
        for obj, (name, descr) in zip(objects, data):
            field_value = getattr(obj, 'text_{}'.format(language))
            # if it's already right translation then ignore
            if field_value == name:
                continue
            # save translation
            setattr(obj, 'text_{}'.format(language), self.format_name(name))
            setattr(obj, 'description_{}'.format(language), self.format_name(descr))
            if commit:
                obj.save(
                    force_update=True,
                    update_fields=[
                        'text_{}'.format(language),
                        'description_{}'.format(language),
                    ],
                )
        return objects
