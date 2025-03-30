import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import connection
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse

from questions.forms import CreateQuestionAnswerForm, CreateQuestionForm
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
        query = {"tags__contains": search.split(",")}
    elif option == "resolved":
        query = {"resolve": True}
    else:
        query = {}
    questions = (
        Question.objects.filter(**query)
        .annotate(like_count=Count("likes"))
        .order_by("-resolve", "-like_count")
    )
    if connection != "postgresql" and option == "tag":
        search
        questions = [
            question
            for question in Question.objects.all()
            if any(tag in search.split(",") for tag in question.tags)
        ]
    return render(
        request,
        "questions/questions_content.html",
        {"questions": questions},
    )


def question(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    user = request.user
    if question is None:
        messages.error(
            request,
            "Pregunta no encontrada",
        )
        return redirect(reverse("questions:questions"))
    if user.is_authenticated and user not in question.views.all():
        question.views.add(user)
        question.save()
    return render(request, "questions/question.html", {"question": question})


def create(request):
    if not request.user.is_authenticated:
        messages.warning(
            request,
            "Tienes tener una cuenta para crear una pregunta",
        )
        return redirect(reverse("users:login"))
    if request.method == "POST":
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags = form.cleaned_data["tags"].split(",")
            unresolved_questions = Question.objects.filter(
                author=request.user,
                resolve=False,
                archive=False,
            )
            if len(unresolved_questions) > 0:
                messages.warning(
                    request,
                    "No se puede crear una nueva pregunta, ya hay una en curso",  # noqa
                )
                return redirect(reverse("questions:questions"))
            Question.objects.create(
                title=title, content=content, author=request.user, tags=tags
            )
            return redirect(reverse("questions:questions"))
        else:
            return render(request, "questions/create.html", {"form": form})
    else:
        title = request.GET.get("title", None)
        content = request.GET.get("content", None)
        form = CreateQuestionForm(
            title=title,
            content=content,
        )
        return render(request, "questions/create.html", {"form": form})


def delete(request, question_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    if question.author != request.user:
        messages.warning(request, "No tienes permisos para esta acción")
        return redirect(reverse("questions:questions"))
    question.delete()
    return redirect(reverse("questions:questions"))


@permission_required(perm="root.view_root", raise_exception=True)
def add_remove_toxic(request, question_id: str):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    question.toxic = not question.toxic
    question.save()
    return redirect(reverse("root:question_details", args=[question_id]))


def add_remove_like(request, question_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Necesitas tener una sesión")
        return redirect(reverse("users:login"))
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    question.save()
    return redirect(reverse("questions:question", args=[question_id]))


@permission_required(perm="root.view_root", raise_exception=True)
def create_answer(request, question_id, edit):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    if question.resolve and not bool(edit):
        messages.info(request, "Pregunta ya resuelta")
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


@permission_required(perm="root.view_root", raise_exception=True)
def delete_root(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    question.delete()
    return redirect(reverse("root:questions"))


@permission_required(perm="root.view_root", raise_exception=True)
def archive(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_ids = data.get("question_ids", [])
        Question.objects.filter(id__in=question_ids).update(archive=True)
        return redirect(reverse("root:questions"))
