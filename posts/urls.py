from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path(
        "like/<int:post_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
    path(
        "comment/<int:post_id>/<str:post_type>/",
        views.comments,
        name="comment",
    ),
]
