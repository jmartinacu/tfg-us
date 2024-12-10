from django.urls import path

from questions import views

app_name = "questions"

urlpatterns = [
    path("", views.questions, name="questions"),
    path("delete/<int:question_id>/", views.delete, name="delete"),
    path(
        "like/<int:question_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
]
