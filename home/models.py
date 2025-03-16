from django.db import models


class ProfileInformation(models.Model):
    name = models.CharField(max_length=255)
    secondary_name = models.CharField(max_length=255, blank=True)
    descriptions = models.JSONField()
    url = models.URLField(blank=True, null=True)
