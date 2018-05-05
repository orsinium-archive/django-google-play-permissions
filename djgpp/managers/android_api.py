# built-in
import os
from pathlib import Path

# external
import requests
from gpapi.googleplay import GooglePlayAPI, RequestError

# django
from django.conf import settings
from django.core.signing import BadSignature, Signer

# app
from ..constants import GROUPS, NULL_OBJECT_NAME, UPPERCASE
from ..models import Permission
from .base import Base


signer = Signer(salt='5omeS@lt4S0meMag!ckO.o')

TEMPLATE = """Please, save these credentials into your project settings:
ANDROID_GSF_ID = {}
ANDROID_AUTH_SUBTOKEN = '{}'
"""


class AndroidAPI(Base):
    def __init__(self, **credentials):
        self.connect(**credentials)
        self.null_object = Permission.objects.get(text=NULL_OBJECT_NAME)

    def connect(self, **credentials):
        """Get credentials and log-in to Google account.
        
        1. Try get credentials from kwargs.
        2. Try get credentials from settings (gsfId and authSubToken).
        3. Try get credentials from credentials.txt (gsfId and authSubToken).
            This file placed into package dir (for avoid adding into VCS from project)
            and signed on SECRET_KEY (for avoid sharing between projects).
        4. Try get credentials from settings (email and password).
        """
        self.api = GooglePlayAPI('en_US', 'Europe/Russia')
        # save credentials to app (not project) folder
        path = os.path.dirname(os.path.abspath(__file__))
        path = Path(path) / 'credentials.txt'

        # auth by credentials from kwargs
        if credentials:
            self.api.login(**credentials)
            self._write_credentials(path, self.api.gsfId, self.api.authSubToken)
            return self

        # auth by credentials from settings
        if getattr(settings, 'ANDROID_GSF_ID', ''):
            self.api.login(
                gsfId=settings.ANDROID_GSF_ID,
                authSubToken=settings.ANDROID_AUTH_SUBTOKEN,
            )
            return self

        # auth by credentials from file into app dir
        if path.exists():
            data = path.open().read()
            try:
                data = signer.unsign(data)
            except BadSignature:
                pass
            else:
                gsf_id, auth_subtoken = data.split('|')
                self.api.login(gsfId=int(gsf_id), authSubToken=auth_subtoken)
                return self

        # auth by login and password
        self.api.login(
            email=settings.ANDROID_EMAIL,
            password=settings.ANDROID_PASSWORD,
        )
        self._write_credentials(path, self.api.gsfId, self.api.authSubToken)
        return self

    @staticmethod
    def _write_credentials(path, gsf_id, auth_subtoken):
        """Write credentials into console and file
        """
        # print data into console
        print(TEMPLATE.format(gsf_id, auth_subtoken))
        # sign and save into file
        data = signer.sign(str(gsf_id) + '|' + auth_subtoken)
        return path.open('w').write(data)

    def download(self, app_id):
        """Get permissions list from API
        """
        path = 'details?doc={}'.format(requests.utils.quote(app_id))
        try:
            response = self.api.executeRequestApi2(path)
        except RequestError:
            return
        return response.payload.detailsResponse.docV2.details.appDetails.permission

    def parse(self, permissions):
        """Convert permissions names list to Permission objects

        1. Iterate over permissions.
        2. Filter non-android permissions.
        3. Convert each permission to Permission object.
        """
        result = []
        for name in permissions:
            # get only android related permissions
            if name.startswith('android.permission.') or name.startswith('com.android.'):
                result.append(self.get_object(name))
        return result

    def get_object(self, name):
        """Get or create 
        """
        obj, _created = Permission.objects.get_or_create(
            text=self.format_name(name),
            defaults=dict(
                parent=self.get_parent(name) or self.null_object,
            ),
        )
        return obj

    @staticmethod
    def format_name(name):
        """Convert slug to display name.
        android.permissions.BROADCAST_SMS -> Broadcast SMS
        """
        # android.permissions.BLUETOOTH_ADMIN -> BLUETOOTH_ADMIN
        name = name.rsplit('.', 1)[-1]
        # BLUETOOTH_ADMIN -> bluetooth admin
        name = name.lower().replace('_', ' ')
        # broadcast sms -> broadcast SMS
        name = ' '.join([UPPERCASE.get(word, word) for word in name.split()])
        # broadcast SMS -> Broadcast SMS
        name = name[0].upper() + name[1:]
        return name

    @staticmethod
    def get_parent(name):
        """Get parent for permission by slug (not converted name)
        """
        name = name.rsplit('.', 1)[-1].lower().replace('_', ' ')

        # find by group name
        for group in GROUPS:
            if group in name:
                return Permission.objects.get(text__iexact=group)

        # find by aliases
        for word in name.split():
            for group, aliases in GROUPS.items():
                if word in aliases:
                    return Permission.objects.get(text__iexact=group)
