from django.contrib import admin
from .utils import TranslationAdmin
from .models import Permission
from .translation import PermissionTO


class PermissionAdmin(TranslationAdmin):
    list_display = ('text', )
    search_fields = ('text', 'description')
    translation_options = PermissionTO


admin.site.register(Permission, PermissionAdmin)
