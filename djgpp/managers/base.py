# built-in
import abc

# external
from googletrans import Translator

# django
from django.utils.translation import override

# app
from ..models import App
from ..utils import requests_retry_session


translator = Translator()


class IBase(metaclass=abc.ABCMeta):
    """Interface for managers.
    Any manager MUST provide this interface.
    Any manager CAN NOT provide any other interface.
    """
    @abc.abstractmethod
    def connect(self, app_id, language='en'):
        pass

    @abc.abstractmethod
    def get(self, app_id, language='en'):
        pass

    @property
    @abc.abstractmethod
    def api(self):
        pass


class Base(IBase):
    api = None

    def __init__(self, **credentials):
        self.connect(**credentials)

    def connect(self, **credentials):
        self.api = requests_retry_session()

    def get(self, app_id, language='en'):
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
        raise NotImplementedError

    @staticmethod
    def parse(data):
        raise NotImplementedError

    def translate(self, objects, language, commit=True):
        for obj in objects:
            field_name = 'name_{}'.format(language)
            field = getattr(obj, field_name)
            if not field:
                field = translator.translate(obj.name_en, src='en', dest=language).text
                if commit:
                    obj.save(force_update=True, update_fields=[field_name])
        return objects

    @staticmethod
    def create_app(app_id, permissions):
        app = App.objects.create(gplay_id=app_id)
        app.permissions.add(*permissions)
        return app
