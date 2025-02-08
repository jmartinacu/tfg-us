from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("/", views.home_images, name="home_images"),
    path("videos/", views.home_videos, name="home_videos"),
    path("tag/<int:tag_id>/", views.home_tag, name="home_tag"),
    path("edit/", views.home_edit_profile, name="home_edit_profile"),
    path("messages/", views.add_message, name="home_message"),
]
