# django
from django.contrib import admin

# app
from .models import Permission


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'description')


admin.site.register(Permission, PermissionAdmin)
