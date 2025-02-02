import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse

from posts.models import Post, Tag
from questions.models import Question
from root.forms import CreateTag, StaffCreationForm, UploadPost


def root(request):
    posts = Post.objects.all().annotate(
        comments=Count("comments"),
    )
    is_postgresql = connection.vendor == "postgresql"
    if is_postgresql:
        from django.contrib.postgres.aggregates import StringAgg

        posts.annotate(
            tags=StringAgg("tags__name", delimiter=","),
        )
    else:
        for post in posts:
            post.tags = ",".join(tag.name for tag in post.tags)
    return render(
        request,
        "root/posts/posts.html",
        {
            "posts": posts,
        },
    )


def users(request):
    users = User.objects.all()
    return render(
        request,
        "root/users/users.html",
        {"users": users},
    )


def tags(request):
    tags = Tag.objects.all()
    return render(
        request,
        "root/tags/tags.html",
        {
            "tags": tags,
        },
    )


def questions(request):
    questions = Question.objects.all()
    return render(
        request,
        "root/questions/questions.html",
        {
            "questions": questions,
        },
    )


def create_admin(request):
    if request.method == "POST":
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            users = User.objects.filter(username=username)
            if users.exists():
                # TODO: messages.warning(request, "El nombre de usuario ya existe")
                return render(
                    request,
                    "root/users/create.html",
                    {
                        "form": form,
                    },
                )
            user = form.save()
            login(request, user)
            return redirect(reverse("root:users"))
    else:
        form = StaffCreationForm()
    return render(
        request,
        "root/users/create.html",
        {
            "form": form,
        },
    )


def upload_post(request):
    if request.method == "POST":
        form = UploadPost(request.POST, request.FILES)
        if form.is_valid():
            try:
                result = Post.objects.create(
                    files=form.cleaned_data["file"],
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["des"],
                )
                return redirect(
                    reverse(
                        "root:post_details",
                        kwargs={"post_id": result["id"]},
                    )
                )
            except ValueError as e:
                upload_post = render(
                    request,
                    "root/posts/create.html",
                    {"form": form},
                )
                if str(e) == "DuplicateName":
                    # TODO: messages.warning(
                    #     request,
                    #     "Ya hay una publicación con ese nombre",
                    # )
                    return upload_post
                elif str(e) == "NoFiles":
                    # TODO: messages.warning(
                    #     request,
                    #     "El archivo tiene que ser una imagen o video",
                    # )
                    return upload_post
                elif str(e) == "FilesError":
                    # TODO: messages.warning(
                    #     request,
                    #     "Solamente se puede subir un video por publicación",
                    # )
                    return upload_post
        else:
            return render(
                request,
                "root/posts/create.html",
                {"form": form},
            )
    else:
        form = UploadPost()
        return render(
            request,
            "root/posts/create.html",
            {"form": form},
        )


def tag_action(request):
    if request.method == "POST" and "file" in request.FILES:
        form = CreateTag(request.POST, request.FILES)
        if form.is_valid():
            name: str = form.cleaned_data["name"]
            ids: str = form.cleaned_data["ids"]
            file = form.cleaned_data["file"]
            posts = Post.objects.filter(id__in=ids.split(","))
            Tag.create(
                name=name,
                file=file,
                posts=posts,
            )
            return redirect(reverse("root:root"))
        return redirect("root:root")
    elif request.method == "GET":
        post_ids = request.GET.get("post_ids", [])
        post_ids = post_ids.split(",")
        posts = Post.objects.filter(id__in=post_ids)
        form = CreateTag(
            ids=",".join(post.id for post in posts),
            init=True,
        )
        return render(
            request,
            "root/tags/create.html",
            {
                "form": form,
                "posts": posts,
            },
        )
    else:
        return redirect(reverse("root:root"))


def delete_action(request, model):
    if request.method == "POST":
        referrer_url = request.META.get("HTTP_REFERER", "/")
        if model not in settings.AUTH_ACTION_MODELS:
            # TODO: messages.error(request, "Acción no permitida")
            return redirect(referrer_url)
        data = json.loads(request.body)
        ids = data.get("delete_ids", [])
        if model == "User":
            if request.user.id in ids:
                # TODO: messages.warning(
                #     request,
                #     "No puedes borrar al usuario que realiza la acción",
                # )
                return redirect(referrer_url)
            User.objects.filter(id__in=ids).delete()
        elif model == "Post":
            Post.objects.filter(id__in=ids).delete()
        elif model == "Tag":
            Tag.objects.filter(id__in=ids).delete()
        elif model == "Question":
            Question.objects.filter(id__in=ids).delete()
        # TODO: messages.success(request, "Acción completada")
        return redirect(referrer_url)
    else:
        # TODO: messages.warning(request, "Acción incorrecta")
        return redirect(reverse("root:root"))


def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        # TODO: messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    post.delete()
    return redirect(reverse("root:root"))


def delete_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user is None:
        # TODO: messages.error(request, "Usuario no encontrado")
        return redirect(reverse("root:users"))
    admins = User.objects.filter(is_staff=True)
    if len(admins) == 1 and admins[0].id == user_id:
        # TODO: messages.warning(
        #     request,
        #     "No se pueden eliminar todos los administradores",
        # )
        return redirect(reverse("root:users"))
    user.delete()
    return redirect(reverse("root:users"))


def delete_tag(request, tag_id):
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        # TODO: messages.error(request, "Etiqueta no encontrado")
        return redirect(reverse("root:tags"))
    tag.delete()
    return redirect(reverse("root:tags"))
