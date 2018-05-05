# built-in
from collections import defaultdict
from functools import partial

# external
import requests
from modeltranslation.admin import TranslationAdmin as _TranslationAdmin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# django
from django.conf import settings

# app
from .constants import NULL_OBJECT_NAME
from .models import Permission


TRANSLATION_TEMPLATE = 'Translations for {}'


def get_field_translations(obj, field):
    langs = []
    for lang, _x in settings.LANGUAGES:
        if getattr(obj, '{}_{}'.format(field, lang), None):
            langs.append(lang)
    return u', '.join(langs)


class TranslationAdmin(_TranslationAdmin):
    def get_list_display(self, request):
        fields = list(self.list_display)
        for field in self.translation_options.fields:
            prop = partial(get_field_translations, field=field)
            prop.short_description = TRANSLATION_TEMPLATE.format(field)
            fields.append(prop)
        return fields


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
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


def group_by_parents(objects):
    """Group Permission objects list by parents.
    """
    null_object = Permission.objects.get(text=NULL_OBJECT_NAME)
    result = defaultdict(list)
    for obj in objects:
        if obj.parent:
            result[obj.parent].append(obj)
        else:
            result[null_object].append(obj)
    return dict(result)
