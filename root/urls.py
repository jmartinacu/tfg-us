from django.urls import path

from root import views

app_name = "root"

urlpatterns = [
    path("", views.root, name="root"),
]
