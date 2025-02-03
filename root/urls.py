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
    path("actions/tag/", views.tag_action, name="tag_action"),
    path(
        "actions/delete/<str:model>/",
        views.delete_action,
        name="delete_action",
    ),
    path("post/delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("user/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("tag/delete/<int:tag_id>/", views.delete_tag, name="delete_tag"),
    path("post/edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/", views.post_details, name="post_details"),
    path("user/<int:user_id>/", views.user_details, name="user_details"),
    path("tag/<int:tag_id>/", views.tag_details, name="tag_details"),
]
