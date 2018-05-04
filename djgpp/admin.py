# django
from django.contrib import admin

# app
from .models import Permission
from .translation import PermissionTO
from .utils import TranslationAdmin


class PermissionAdmin(TranslationAdmin):
    list_display = ('text', )
    search_fields = ('text', 'description')
    translation_options = PermissionTO


admin.site.register(Permission, PermissionAdmin)
