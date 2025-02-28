from django.db import models


class Root(models.Model):
    name = models.CharField(max_length=255)
