# app
from .android_api import AndroidAPI
from .base import Base


class PermissionManager(Base):
    def __init__(self, apis=(AndroidAPI, )):
        self.apis = [api() for api in apis]

    def get(self, app_id, language='en'):
        for api in self.apis:
            permissions = api.get(app_id, language)
            if permissions:
                return permissions
