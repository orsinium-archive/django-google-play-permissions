# app
from .android_api import AndroidAPI
from .base import Base
from .mobile_api import MobileAPI
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
    api = None
    apis = ()

    def __init__(self, api=MobileAPI, apis=(WebAPI, WebInterface, AndroidAPI)):
        self.api = api
        self.apis = apis
        self.connect()

    def connect(self, **credentials):
        """Connect to servers
        """
        if self.api:
            self.api = self.api()
        self.apis = [api() for api in self.apis]

    def get(self, app_id, language='en'):
        """Get translated permissions as Permission objects list.
        """
        # Only MobileAPI can get right translation and descriptions.
        # But MobileAPI can't detect groups. We need other managers for it.
        if self.api:
            self.api.get(app_id, language)
        for api in self.apis:
            permissions = api.get(app_id, language)
            if permissions:
                return permissions
