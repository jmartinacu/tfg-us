import tempfile
from io import BytesIO
from os import path
from urllib.error import HTTPError
from urllib.parse import urlparse

import imageio
import magic
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from PIL import Image

from home.models import ProfileInformation
from samer.bucket import delete_file as bucket_delete
from samer.bucket import upload_file, upload_thumbnail


class FilesTypes(models.TextChoices):
    IMAGE = "IM", _("Image")
    VIDEO = "VD", _("Video")


class PostManager(models.Manager):

    def create(self, *args, **kwargs):
        files = kwargs.pop("files", None)
        name = kwargs.get("name", None)
        if files is None:
            raise ValueError("NoFiles")
        if name is None:
            full_file_name = str(files[0].name)
            file_name, _ext = path.splitext(full_file_name)
            kwargs["name"] = file_name
        check_name = Post.objects.filter(name=name)
        if check_name.exists():
            raise ValueError("DuplicateName")
        post: Post = super().create(*args, **kwargs)
        try:
            post.create_sources(files)
        except ValueError as e:
            post.delete()
            raise e
        return post


class Post(models.Model):
    name = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    description = models.TextField(blank=True, null=True)

    objects = PostManager()

    def tag_names(self):
        res = ""
        if self.tags.exists():
            res = ", ".join([tag.name for tag in self.tags.all()])
        return res

    def create_sources(self, files):
        sources: list[Source] = []
        for file in files:
            post_bytes = file.read()
            file.seek(0)
            src = Source(file=file, file_bytes=post_bytes, post=self)
            sources.append(src)
        if len(
            sources,
        ) > 1 and not all(s.type != FilesTypes.IMAGE for s in sources):
            for src in sources:
                src.delete()
            raise ValueError("FilesError")
        Source.objects.bulk_create(sources)

    def __str__(self):
        return self.name


class TagManager(models.Manager):

    def create(self, *args, **kwargs):
        file = kwargs.pop("file", None)
        if file is None:
            raise ValueError("NoFile")
        tag = super().create(*args, **kwargs)
        post_bytes = file.read()
        file.seek(0)
        src = Source(file=file, file_bytes=post_bytes, tag=tag)
        src.save()
        return tag

    def delete(self):
        # Execute delete for each Tag instance and its related sources
        return super().delete()


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name="tags")

    objects = TagManager()

    def __str__(self):
        return self.name


class Source(models.Model):
    url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=2,
        choices=FilesTypes.choices,
    )
    extension = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="tag_source",
        null=True,
    )
    profile = models.ForeignKey(
        ProfileInformation,
        on_delete=models.CASCADE,
        related_name="profile_source",
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="sources",
        null=True,
    )

    def get_mime_type(self, url=None):
        response = requests.get(url or self.url, stream=True, timeout=10)
        response.raise_for_status()
        mime = magic.Magic(mime=True)
        result = mime.from_buffer(response.raw.read(1024))
        response.close()
        return result

    def get_file_bytes(self, thumbnail=False):
        url = self.thumbnail_url if thumbnail else self.url
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content

    def is_image(self, bytes=None):
        try:
            Image.open(BytesIO(bytes or self.get_file_bytes()))
            return True
        except IOError:
            return False

    def is_video(self):
        with tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=True,
        ) as temp_file:
            temp_file.write(self.get_file_bytes())
            temp_file.flush()
            reader = imageio.get_reader(temp_file.name)
            try:
                _ = reader.get_next_data()
                is_video_file = True
            except RuntimeError:
                is_video_file = False
            reader.close()
            return is_video_file

    def __init__(self, *args, **kwargs):
        if "id" in kwargs or args:
            return super().__init__(*args, **kwargs)
        file = kwargs.pop("file", None)
        file_bytes = kwargs.pop("file_bytes", None)
        if file is None or file_bytes is None:
            raise ValueError("NoFile")
        full_file_name = str(file.name)
        file_name, ext = path.splitext(full_file_name)
        check_name = Source.objects.filter(name=file_name)
        if check_name.exists():
            raise ValueError("DuplicateName")
        file_type = (
            FilesTypes.IMAGE
            if self.is_image(
                file_bytes,
            )
            else FilesTypes.VIDEO
        )
        if "tag" in kwargs and kwargs["tag"] is not None:
            if file_type == FilesTypes.VIDEO:
                raise ValueError("FileError")
            object_name = f"tags/{full_file_name}"
        elif "profile" in kwargs and kwargs["profile"] is not None:
            if file_type == FilesTypes.VIDEO:
                raise ValueError("FileError")
            object_name = f"{full_file_name}"
        else:
            object_name = (
                f"imagenes/{full_file_name}"
                if file_type == FilesTypes.IMAGE
                else f"videos/{full_file_name}"
            )
        uploaded_file_url = upload_file(
            file,
            object_name=object_name,
        )
        try:
            mime_type = self.get_mime_type(uploaded_file_url)
        except HTTPError:
            raise ValueError("HttpError")
        thumbnail_url = None
        if file_type == FilesTypes.VIDEO:
            thumbnail_url = upload_thumbnail(0, uploaded_file_url)
        kwargs["url"] = uploaded_file_url
        kwargs["name"] = file_name
        kwargs["type"] = file_type
        kwargs["thumbnail_url"] = thumbnail_url
        kwargs["extension"] = ext
        kwargs["mime_type"] = mime_type
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Source)
def delete_file(sender, instance, **kwargs):
    if not instance.url:
        return
    parsed_url = urlparse(instance.url)
    if instance.thumbnail_url:
        parsed_thumb_url = urlparse(instance.thumbnail_url)
        if settings.AWS_BUCKET_NAME in parsed_thumb_url.netloc:
            bucket_delete(parsed_thumb_url.path[1:])
    if settings.AWS_BUCKET_NAME not in parsed_url.netloc:
        return
    bucket_delete(parsed_url.path[1:])


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
        null=True,
    )
    toxic = models.BooleanField(default=False)
    moderate = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment for {self.post.name}"
