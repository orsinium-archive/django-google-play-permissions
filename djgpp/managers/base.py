import abc
from googletrans import Translator
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
        data = self.download(app_id, language)
        objects = self.parse(data)
        return self.translate(objects, language)

    def download(self, app_id, language):
        raise NotImplementedError

    @staticmethod
    def parse(data):
        raise NotImplementedError

    def translate(self, objects, language):
        raise NotImplementedError
        # translator.translate(src='en', dest=language).text
