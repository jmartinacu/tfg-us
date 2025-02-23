from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    resolve = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    toxic = models.BooleanField(default=False)
    moderate = models.BooleanField(default=False)
    answer = models.OneToOneField(
        "Answer", on_delete=models.SET_NULL, null=True, blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name="liked_questions",
        blank=True,
        null=True,
    )
    tags = models.JSONField(default=list)
    views = models.ManyToManyField(
        User,
        related_name="viewed_questions",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer to {self.question.title}"
