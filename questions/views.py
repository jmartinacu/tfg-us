from django.shortcuts import redirect, render
from django.urls import reverse

from questions.models import Question


def questions(request):
    option = request.GET.get("option", "")
    search = request.GET.get("search", "")
    if option == "author":
        query = {"author__username__startswith": search}
    elif option == "content":
        query = {"content__icontains": search}
    elif option == "title":
        query = {"title__startswith": search}
    elif option == "tag":
        query = {"tags__in": search.split(",")}
    elif option == "resolved":
        query = {"resolve": True}
    else:
        query = {}
    questions = Question.objects.filter(**query)
    return render(
        request,
        "questions/questions_content.html",
        {"questions": questions},
    )


def delete(request, question_id):
    if not request.user.is_authenticated:
        # TODO: messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        # TODO: messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    if question.author != request.user:
        # TODO: messages.warning(request, "No tienes permisos para esta acción")
        return redirect(reverse("questions:questions"))
    question.delete()
    return redirect(reverse("questions:questions"))
