from django.db import models

from posts.models import Source


class ProfileInformationManager(models.Manager):

    def create(self, *args, **kwargs):
        file = kwargs.pop("file", None)
        if file is None:
            raise ValueError("NoFile")
        profile = super().create(*args, **kwargs)
        post_bytes = file.read()
        file.seek(0)
        src = Source(file=file, file_bytes=post_bytes, profile=profile)
        src.save()
        return profile


class ProfileInformation(models.Model):

    objects = ProfileInformationManager()

    name = models.CharField(max_length=255)
    secondary_name = models.CharField(max_length=255, blank=True)
    descriptions = models.JSONField()
    url = models.URLField(blank=True, null=True)
