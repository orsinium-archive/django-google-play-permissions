# app
from .android_api import AndroidAPI
from .base import Base
from .web_api import WebAPI
from .web_interface import WebInterface


class PermissionManager(Base):
    """Core permissions manager.
    
    Manipulate other managers and get better result.

    Default resolution order:
    1. WebAPI -- preferred, but reversed and can be broken anytime.
    1. WebInterface -- good, but use interface and can be broken anytime.
        And this is slow, yeah.
    1. AndroidAPI -- good and safe, but different from Google Play interface.
    """
    def __init__(self, apis=(WebAPI, WebInterface, AndroidAPI, )):
        self.apis = [api() for api in apis]

    def get(self, app_id, language='en'):
        """Get translated permissions as Permission objects list.
        """
        for api in self.apis:
            permissions = api.get(app_id, language)
            if permissions:
                return permissions
