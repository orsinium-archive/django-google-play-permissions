from django.db import models


class Permission(models.Model):
    text = models.TextField()
    description = models.TextField(blank=True, default='')
    # if parent is NULL then permission is category (root permission)
    parent = models.ForeignKey('self', null=True)


class App(models.Model):
    gplay_id = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField(Permission)
