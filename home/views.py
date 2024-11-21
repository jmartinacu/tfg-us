from django.db.models import Count
from django.shortcuts import render

from posts.models import Post


def home_images(request):
    posts = Post.objects.filter(
        post_type=Post.PostTypes.IMAGE,
    ).annotate(
        comments=Count("comments"),
    )
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )


def home_videos(request):
    posts = Post.objects.filter(
        post_type=Post.PostTypes.VIDEO,
    ).annotate(
        comments=Count("comments"),
    )
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )
