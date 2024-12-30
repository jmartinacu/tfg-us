from django.urls import path

from questions import views

app_name = "questions"

urlpatterns = [
    path("", views.questions, name="questions"),
    path("create/", views.create, name="create"),
    path("archive/", views.archive, name="archive"),
    path("delete/<int:question_id>/", views.delete, name="delete"),
    path(
        "create/answer/<int:question_id>/<str:edit>/",
        views.create_answer,
        name="create_answer",
    ),
    path(
        "like/<int:question_id>/",
        views.add_remove_like,
        name="add_remove_like",
    ),
]
