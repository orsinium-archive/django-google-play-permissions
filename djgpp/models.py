import re
# django
from django.utils.translation import get_language
from django.conf import settings
from django.db import models


REX_WORD = re.compile(r'[a-z0-9-]+')


class Permission(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    name = models.TextField()

    @property
    def is_category(self):
        return not self.parent

    @property
    def translation(self):
        lang = get_language()
        return self.translation_set.filter(language=lang).first()

    def __str__(self):
        return self.name

    def get_icon_url(self):
        if not self.is_category:
            return
        slug = REX_WORD.search(self.name.lower()).group()
        return '{}djgpp/{}.png'.format(settings.STATIC_URL, slug)


class Translation(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

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
