# built-in
import abc
from itertools import chain

# external
from googletrans import Translator

# django
from django.utils.translation import override

# app
from ..models import App


translator = Translator()


class IBase(metaclass=abc.ABCMeta):
    """Interface for managers.

    Any manager MUST provide this interface.
    Any manager CAN NOT provide any other interface.
    """
    @abc.abstractmethod
    def connect(self, app_id, language='en'):
        """Connect to server
        """
        pass

    @abc.abstractmethod
    def get(self, app_id, language='en'):
        """Get translated permissions as objects list.
        """
        pass

    @property
    @abc.abstractmethod
    def api(self):
        """Contain connection

        For example, requests session.
        """
        pass


class Base(IBase):
    api = None

    def __init__(self, **credentials):
        self.connect(**credentials)

    def get(self, app_id, language='en'):
        """Get translated permissions as objects list.
        """
        # get from database
        app = App.objects.filter(gplay_id=app_id).first()
        if app:
            objects = list(app.permissions.all())
            return self.translate(objects, language)

        # get from manager
        with override('en'):
            data = self.download(app_id)
            if not data:
                return
            objects = self.parse(data)
            self.create_app(app_id, objects)
            return self.translate(objects, language)

    def download(self, app_id, language):
        """Download and extract raw permissions data from server
        """
        raise NotImplementedError

    @staticmethod
    def parse(data):
        """Convert raw permissions data to Permission objects list
        """
        raise NotImplementedError

    def translate(self, objects, language, commit=True):
        """Translate permission objects list to language (if not translated)
        """
        parents = [obj.parent for obj in objects if obj.parent]
        for obj in chain(objects, parents):
            field_name = 'text_{}'.format(language)
            field_value = getattr(obj, field_name)
            if not field_value:
                translation = translator.translate(obj.text_en, src='en', dest=language).text
                setattr(obj, field_name, translation[0].upper() + translation[1:])
                if commit:
                    obj.save(force_update=True, update_fields=[field_name])
        return objects

    @staticmethod
    def create_app(app_id, permissions):
        """Create app object with permissions into database
        """
        app = App.objects.create(gplay_id=app_id)
        app.permissions.add(*permissions)
        return app
