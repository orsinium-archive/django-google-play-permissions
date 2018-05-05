# django
from django.conf import settings
from django.db import models


class Permission(models.Model):
    text = models.TextField()
    description = models.TextField(blank=True, default='')
    # if parent is NULL then permission is category (root permission)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_icon_url(self):
        if not self.parent:
            return
        slug = self.name.lower.replace(' ', '_')
        return '{}djgpp/{}.png'(settings.STATIC_URL, slug)


class App(models.Model):
    gplay_id = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.gplay_id

