# built-in
import json
from collections import OrderedDict, defaultdict
from functools import lru_cache

# external
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# project
from googletrans import Translator

# app
from .models import App, Permission, Translation


translator = Translator()


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
            return self.sort(result, language)

        names = self.get_names(app_id)
        names_tr = self.get_names(app_id, language)

        groups = self.get_groups(app_id)
        groups_tr = self.get_groups(app_id, language)

        result = self.combine(names, names_tr, groups, groups_tr, language)
        return self.sort(result, language)

    @staticmethod
    def get_from_database(app_id, language='en'):
        # get app
        app = App.objects.filter(gplay_id=app_id).first()
        if not app:
            return
        # get permissions
        permissions = app.permissions.filter(language=language)
        if not permissions:
            return
        # group
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
        if len(data) > 2:
            data[1][-1][-1].extend(data[-1])
        # get permissions
        result = {}
        for group, _info, permissions in (data[0] + data[1])[1:]:
            for permission in permissions:
                result[permission[-1]] = group
        return result

    @staticmethod
    @lru_cache(maxsize=8)
    def translate(text, language):
        return translator.translate(text, src='en', dest=language).text

    @classmethod
    def combine(cls, names, names_tr, groups, groups_tr, language):
        result = defaultdict(list)
        for (name, descr), (name_tr, descr_tr) in zip(names, names_tr):
            # get group
            group_name = groups.get(name, 'Other')
            group = Permission.objects.filter(name=group_name).first()
            if not group:
                group = Permission.objects.create(
                    name=group_name,
                )
            if not group.translation_set.filter(language=language):
                group_name_tr = groups_tr.get(name)
                if not group_name_tr:
                    group_name_tr = cls.translate(group_name, language)
                Translation.objects.create(
                    language=language,
                    name=group_name_tr,
                    description='',
                    permission=group,
                )

            # get permission
            obj = Permission.objects.filter(name=name).first()
            if not obj:
                obj = Permission.objects.create(
                    name=name,
                    parent=group,
                )
            if not obj.translation_set.filter(language=language):
                Translation.objects.create(
                    language=language,
                    name=name_tr,
                    description=descr_tr,
                    permission=obj,
                )

            result[group].append(obj)
        return result

    @staticmethod
    def sort(data, language='en'):
        def key(obj):
            if obj.name == 'Other':
                return '\xffff'
            obj = obj.translation_set.filter(language=language).first()
            if not obj:
                return ''
            return obj.name

        # sort groups
        data = OrderedDict(sorted(data.items(), key=lambda x: key(x[0])))
        # sort permissions
        for k, v in data.items():
            v.sort(key=key)
        return data
