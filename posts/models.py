from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class PostTypes(models.TextChoices):
        IMAGE = "IM", _("Image")
        VIDEO = "VD", _("Video")

    name = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    description = models.TextField(blank=True, null=True)
    post_type = models.CharField(
        max_length=2,
        choices=PostTypes,
        default=PostTypes.IMAGE,
    )

    def __str__(self):
        return self.name


class PostSource(models.Model):
    url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="sources",
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return f"Comment for {self.post.name}"
