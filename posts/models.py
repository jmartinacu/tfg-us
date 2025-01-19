import magic
import requests
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Source(models.Model):
    url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)

    def get_mime_type(self):
        result = None
        response = requests.get(self.url, stream=True, timeout=10)
        response.raise_for_status()
        mime = magic.Magic(mime=True)
        result = mime.from_buffer(response.raw.read(1024))
        response.close()
        return result

    def __str__(self):
        return self.name


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
    sources = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="post",
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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return f"Comment for {self.post.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name="tags")
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="tag",
    )

    def __str__(self):
        return self.name
