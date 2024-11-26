from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class PostTypes(models.TextChoices):
        IMAGE = "IM", _("Image")
        VIDEO = "VD", _("Video")

    name = models.CharField(max_length=255)
    object_names = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )
    urls = ArrayField(models.URLField(), blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    likes = ArrayField(models.CharField(max_length=100), blank=True)
    description = models.TextField(blank=True, null=True)
    post_type = models.CharField(
        max_length=2,
        choices=PostTypes,
        default=PostTypes.IMAGE,
    )


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
