from django.contrib.postgres.fields import ArrayField
from django.db import models


class ProfileInformation(models.Model):
    app_name = models.CharField(max_length=255)
    app_real_name = models.CharField(max_length=255)
    descriptions = ArrayField(models.CharField(max_length=100), blank=True)
    url = models.URLField(blank=True, null=True)
    image_url = models.URLField()
