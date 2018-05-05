from collections import defaultdict, OrderedDict
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from .models import Permission, Translation, App


class PermissionController(object):
    mobile_api_url = 'https://play.google.com/store/xhr/getdoc?authuser=0'
    web_api_url = 'https://play.google.com/_/PlayStoreUi/data'
    web_api_template = '[[[163726509,[{"163726509":[[null,["$",7],[]]]}],null,null,0]]]'

    api = None

    def __init__(self, **credentials):
        self.connect(**credentials)

    def connect(self, **credentials):
        """Get requests session
        """
        self.api = self.requests_retry_session()

    @staticmethod
    def requests_retry_session(retries=3, backoff_factor=0.3,
                               status_forcelist=(500, 502, 504), session=None):
        """Make session that retry request on error
        """
        # get session
        session = session or requests.Session()
        # make retry rule
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        # make adapter
        adapter = HTTPAdapter(max_retries=retry)
        # mount adapter to session
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get(self, app_id, language='en'):
        result = self.get_from_database(app_id, language)
        if result:
            return self.sort(result)

        names = self.get_names(app_id)
        names_tr = self.get_names(app_id, language)

        groups = self.get_groups(app_id)
        groups_tr = self.get_groups(app_id, language)

        result = self.combine(names, names_tr, groups, groups_tr, language)
        return self.sort(result)

    def get_from_database(app_id, language='en'):
        app = App.objects.filter(app_id).first()
        if not app:
            return
        permissions = app.permissions.all()
        if not permissions:
            return

        result = defaultdict(list)
        for obj in permissions:
            result[obj.parent].append(obj)
        return result

    def get_names(self, app_id, language='en'):
        response = self.api.post(
            self.mobile_api_url,
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

    def get_groups(self, app_id, language='en'):
        response = self.api.post(
            self.web_api_url,
            params={'hl': language},
            data={'f.req': self.web_api_template.replace('$', app_id)},
        )
        # strip junk from response body begining and decode
        data = json.loads(response.text.split('\n', 1)[-1])
        # get only permissions lists
        data = list(data[0][2].values())[0]
        # concat permissions without group to "Other" group
        data[1][-1][-1].extend(data[-1])
        # get permissions
        result = {}
        for group, _info, permissions in (data[0] + data[1])[1:]:
            for permission in permissions:
                result[permission[-1]] = group
        return result

    @staticmethod
    def combine(names, names_tr, groups, groups_tr, language):
        result = defaultdict(list)
        for (name, descr), (name_tr, descr_tr) in zip(names, names_tr):
            # get group
            group = Permission.objects.filter(name=groups[name]).first()
            if not group:
                group_tr = Translation.objects.create(
                    name=groups_tr[name],
                    description='',
                )
                group = Permission.objects.create(
                    name=groups[name],
                    translation=group_tr,
                )

            # get permission
            obj = Permission.objects.filter(name=name).first()
            if not obj:
                obj_tr = Translation.objects.create(
                    name=name_tr,
                    description=descr_tr,
                )
                group = Permission.objects.create(
                    name=name,
                    translation=obj_tr,
                    parent=group,
                )

            result[group].append(obj)
        return result

    @staticmethod
    def sort(data, language):
        def key(obj):
            if obj.name == 'Other':
                return b'\xffff'
            return obj.translation_set.filter(language=language).first()

        # sort groups
        data = OrderedDict(sorted(data.items(), key=key))
        # sort permissions
        for k, v in data.items():
            v.sort(key=key)
        return data
