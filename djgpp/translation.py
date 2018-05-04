from modeltranslation.translator import TranslationOptions, translator
from .models import Permission


class PermissionTO(TranslationOptions):
    fields = ('text', 'description')


translator.register(Permission, PermissionTO)
