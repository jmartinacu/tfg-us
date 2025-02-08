from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path(
        "like/<int:post_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
    path("search/", views.search_posts, name="search_posts"),
    path(
        "tag/add/<int:tag_id>/",
        views.add_post_to_tag,
        name="add_posts_tag",
    ),
    path(
        "comment/remove/<int:post_id>/<int:comment_id>/",
        views.remove_comment,
        name="remove_comment",
    ),
    path(
        "comment/<int:post_id>/<str:post_type>/",
        views.comments,
        name="comment",
    ),
]
