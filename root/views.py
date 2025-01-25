from django.db import connection
from django.db.models import Count
from django.shortcuts import render

from posts.models import Post


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
