# django
from django.conf import settings
from django.db import models


class Permission(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    name = models.TextField()

    @property
    def is_category(self):
        return not self.parent

    def __str__(self):
        return self.name

    def get_icon_url(self):
        if not self.parent:
            return
        slug = self.name.lower.replace(' ', '_')
        return '{}djgpp/{}.png'(settings.STATIC_URL, slug)


class Translation(models.Model):
    language = models.CharField(max_length=5)
    name = models.TextField()
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class App(models.Model):
    gplay_id = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.gplay_id
