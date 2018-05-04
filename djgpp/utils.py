import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
from functools import partial
from modeltranslation.admin import TranslationAdmin as _TranslationAdmin


def get_field_translations(obj, field):
    langs = []
    for lang, _x in settings.LANGUAGES:
        if getattr(obj, '{}_{}'.format(field, lang), None):
            langs.append(lang)
    return u', '.join(langs)


TRANSLATION_TEMPLATE = 'Translations for {}'


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
