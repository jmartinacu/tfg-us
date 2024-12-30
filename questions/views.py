import json

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


def question(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        # TODO: messages.error(
        #     request,
        #     "Pregunta no encontrada",
        # )
        return redirect(reverse("questions:questions"))
    if request.user.is_authenticated and request.user in question.views.all():
        question.views.add(request.user)
    return render(request, "questions/question.html", {"question": question})


def create(request):
    if not request.user.is_authenticated:
        # TODO: messages.warning(
        #     request,
        #     "Tienes tener una cuenta para crear una pregunta",
        # )
        return redirect(reverse("users:login"))
    if request.method == "POST":
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags: str = form.cleaned_data["tags"]
            author = form.cleaned_data["author"]
            tags = tags.split(",")
            unresolved_questions = Question.objects.filter(
                author=author,
                resolve=False,
                archive=False,
            )
            if len(unresolved_questions) > 0:
                # TODO: messages.warning(
                #     request,
                #     "No se puede crear una nueva pregunta, ya hay una en curso",  # noqa
                # )
                return redirect(reverse("questions:questions"))
            Question.objects.create(
                title=title, content=content, author=author, tags=tags
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
            username=request.user.username,
        )
        return render(request, "questions/create.html", {"form": form})


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


def delete_root(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        #  TODO:messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    question.delete()
    return redirect(reverse("root:questions"))


def archive(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_ids = data.get("question_ids", [])
        Question.objects.filter(id__in=question_ids).update(archive=True)
        return redirect(reverse("root:questions"))
