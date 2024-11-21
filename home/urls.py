from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("", views.home_images, name="home_images"),
    path("videos/", views.home_videos, name="home_videos"),
]
