from django.db import models

from posts.models import Source


class ProfileInformation(models.Model):
    name = models.CharField(max_length=255)
    secondary_name = models.CharField(max_length=255, blank=True)
    descriptions = models.JSONField()
    source = models.OneToOneField(
        Source,
        on_delete=models.CASCADE,
        related_name="profile_information",
        null=True,
    )
    url = models.URLField(blank=True, null=True)
