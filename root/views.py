from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count
from django.shortcuts import render

from posts.models import Post, Tag
from questions.models import Question


def root(request):
    posts = Post.objects.all().annotate(
        comments=Count("comments"),
    )
    is_postgresql = connection.vendor == "postgresql"
    if is_postgresql:
        from django.contrib.postgres.aggregates import StringAgg

        posts.annotate(
            tags=StringAgg("tags__name", delimiter=","),
        )
    else:
        for post in posts:
            post.tags = ",".join(tag.name for tag in post.tags)
    return render(
        request,
        "root/posts/posts.html",
        {
            "posts": posts,
        },
    )


def users(request):
    users = User.objects.all()
    return render(
        request,
        "root/users/users.html",
        {"users": users},
    )


def tags(request):
    tags = Tag.objects.all()
    return render(
        request,
        "root/tags/tags.html",
        {
            "tags": tags,
        },
    )


def questions(request):
    questions = Question.objects.all()
    return render(
        request,
        "root/questions/questions.html",
        {
            "questions": questions,
        },
    )
