from django.urls import path

from root import views

app_name = "root"

urlpatterns = [
    path("", views.root, name="root"),
    path("users/", views.users, name="users"),
    path("tags/", views.tags, name="tags"),
    path("questions/", views.questions, name="questions"),
    path("users/admin/", views.create_admin, name="create_admin"),
]
