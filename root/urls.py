from django.urls import path

from root import views

app_name = "root"

urlpatterns = [
    path("", views.root, name="root"),
    path("users/", views.users, name="users"),
    path("tags/", views.tags, name="tags"),
    path("questions/", views.questions, name="questions"),
    path("users/admin/", views.create_admin, name="create_admin"),
    path("post/upload/", views.upload_post, name="upload_post"),
    path(
        "actions/tag/",
        views.tag_action,
        name="tag_action",
    ),
    path(
        "actions/delete/<str:model>/",
        views.delete_action,
        name="delete_action",
    ),
]
