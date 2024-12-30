from django.shortcuts import redirect, render
from django.urls import reverse

from questions.forms import CreateQuestionAnswerForm
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


def add_remove_like(request, question_id):
    if not request.user.is_authenticated:
        # TODO: messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        # TODO: messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    if question.likes.filter(id=request.user.id).exists:
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    return redirect(reverse("questions:question", args=[question_id]))


def create_answer(request, question_id, edit):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        # TODO: messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    if question.resolve and not bool(edit):
        # TODO: messages.info(request, "Pregunta ya resuelta")
        return redirect(reverse("root:questions"))
    if request.method == "POST":
        form = CreateQuestionAnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data["answer"]
            admin = form.cleaned_data["admin"]
            question.update(
                answer={
                    "admin": admin,
                    "text": answer,
                },
            )
            return redirect(
                reverse("root:question_details", args=[question.id]),
            )
        else:
            return render(
                request,
                "root/questions/create_answer.html",
                {"form": form, "edit": edit, "question": question},
            )
    else:
        form = CreateQuestionAnswerForm(
            admin=request.user.username,
            question=question.content,
        )
        return render(
            request,
            "root/questions/create_answer.html",
            {"form": form, "edit": edit, "question": question},
        )
