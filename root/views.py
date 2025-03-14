import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.shortcuts import redirect, render
from django.urls import reverse

from posts.models import Comment, Post, Tag
from questions.models import Question
from root.forms import CreateTag, EditPost, StaffCreationForm, UploadPost


@permission_required(perm="root.view_root", raise_exception=True)
def root(request):
    posts = Post.objects.all()
    return render(
        request,
        "root/posts/posts.html",
        {"posts": posts},
    )


@permission_required(perm="root.view_root", raise_exception=True)
def users(request):
    users = User.objects.all()
    for user in users:
        user.is_samer_staff = user.has_perm("root.view_root")
    return render(
        request,
        "root/users/users.html",
        {"users": users},
    )


@permission_required(perm="root.view_root", raise_exception=True)
def tags(request):
    tags = Tag.objects.all()
    return render(
        request,
        "root/tags/tags.html",
        {
            "tags": tags,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def questions(request):
    questions = Question.objects.all()
    return render(
        request,
        "root/questions/questions.html",
        {
            "questions": questions,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def create_admin(request):
    if request.method == "POST":
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            users = User.objects.filter(username=username)
            if users.exists():
                messages.warning(request, "El nombre de usuario ya existe")
                return render(
                    request,
                    "root/users/create.html",
                    {
                        "form": form,
                    },
                )
            form.save()
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


@permission_required(perm="root.view_root", raise_exception=True)
def upload_post(request):
    if request.method == "POST":
        form = UploadPost(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = Post.objects.create(
                    files=form.cleaned_data["file"],
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["des"],
                )
                return redirect(
                    reverse(
                        "root:post_details",
                        kwargs={"post_id": post.id},
                    )
                )
            except ValueError as e:
                upload_post = render(
                    request,
                    "root/posts/create.html",
                    {"form": form},
                )
                if str(e) == "DuplicateName":
                    messages.warning(
                        request,
                        "Ya hay una publicación con ese nombre",
                    )
                    return upload_post
                elif str(e) == "NoFiles":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return upload_post
                elif str(e) == "FilesError":
                    messages.warning(
                        request,
                        "Solamente se puede subir un video por publicación",
                    )
                    return upload_post
                elif str(e) == "HttpError":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
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


@permission_required(perm="root.view_root", raise_exception=True)
def tag_action(request):
    if request.method == "POST" and "file" in request.FILES:
        form = CreateTag(request.POST, request.FILES)
        if form.is_valid():
            name: str = form.cleaned_data["name"]
            ids: str = form.cleaned_data["ids"]
            file = form.cleaned_data["file"]
            posts = Post.objects.filter(id__in=ids.split(","))
            try:
                tag = Tag.objects.create(
                    name=name,
                    file=file,
                )
                tag.posts.set(posts)
                return redirect(reverse("root:root"))
            except ValueError as e:
                render_create_tag = render(
                    request,
                    "root/tags/create.html",
                    {
                        "form": form,
                        "posts": posts,
                    },
                )
                if str(e) == "NoFile":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return render_create_tag
        return redirect("root:root")
    elif request.method == "GET":
        post_ids = request.GET.get("post_ids", [])
        post_ids = post_ids.split(",")
        posts = Post.objects.filter(id__in=post_ids)
        if posts.count() != len(post_ids):
            messages.error(request, "Publicaciones no encontradas")
            return redirect(reverse("root:root"))
        form = CreateTag(
            ids=",".join(post_ids),
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


@permission_required(perm="root.view_root", raise_exception=True)
def delete_action(request, model):
    if request.method == "POST":
        referrer_url = request.META.get("HTTP_REFERER", "/")
        if model not in settings.AUTH_ACTION_MODELS:
            messages.error(request, "Acción no permitida")
            return redirect(referrer_url)
        data = json.loads(request.body)
        ids = data.get("delete_ids", [])
        if model == "User":
            if request.user.id in ids:
                messages.warning(
                    request,
                    "No puedes borrar al usuario que realiza la acción",
                )
                return redirect(referrer_url)
            User.objects.filter(id__in=ids).delete()
        elif model == "Post":
            Post.objects.filter(id__in=ids).delete()
        elif model == "Tag":
            Tag.objects.filter(id__in=ids).delete()
        elif model == "Question":
            Question.objects.filter(id__in=ids).delete()
        messages.success(request, "Acción completada")
        return redirect(referrer_url)
    else:
        messages.warning(request, "Acción incorrecta")
        return redirect(reverse("root:root"))


@permission_required(perm="root.view_root", raise_exception=True)
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    post.delete()
    return redirect(reverse("root:root"))


@permission_required(perm="root.view_root", raise_exception=True)
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user is None:
        messages.error(request, "Usuario no encontrado")
        return redirect(reverse("root:users"))
    admins = User.objects.filter(is_staff=True)
    if len(admins) == 1 and admins[0].id == user_id:
        messages.warning(
            request,
            "No se pueden eliminar todos los administradores",
        )
        return redirect(reverse("root:users"))
    user.delete()
    return redirect(reverse("root:users"))


@permission_required(perm="root.view_root", raise_exception=True)
def delete_tag(request, tag_id):
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        messages.error(request, "Etiqueta no encontrado")
        return redirect(reverse("root:tags"))
    tag.delete()
    return redirect(reverse("root:tags"))


@permission_required(perm="root.view_root", raise_exception=True)
def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    if request.method == "POST":
        form = EditPost(request.POST, request.FILES)
        if form.is_valid():
            try:
                if "file" in request.FILES:
                    files = form.cleaned_data["file"]
                    post.sources.all().delete()
                    sources = Post.create_sources(files)
                    post.sources.add(*sources)
                post.name = form.cleaned_data["name"]
                post.description = form.cleaned_data["des"]
                post.save()
            except ValueError as e:
                form = EditPost(post=post)
                render_edit = render(
                    request,
                    "root/posts/edit.html",
                    {
                        "form": form,
                        "post": post,
                    },
                )
                if str(e) == "DuplicateName":
                    messages.warning(
                        request,
                        "Ya hay una publicación con ese nombre",
                    )
                    return render_edit
                elif str(e) == "NoFiles":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return render_edit
                elif str(e) == "FilesError":
                    messages.warning(
                        request,
                        "Solamente se puede subir un video por publicación",
                    )
                    return render_edit
                elif str(e) == "HttpError":
                    messages.warning(
                        request,
                        "El archivo tiene que ser una imagen o video",
                    )
                    return render_edit
            return redirect(
                reverse(
                    "root:post_details",
                    kwargs={"post_id": post_id},
                )
            )
        else:
            return render(
                request,
                "root/posts/edit.html",
                {
                    "form": form,
                    "post": post,
                },
            )
    else:
        form = EditPost(post=post)
        return render(
            request,
            "root/posts/edit.html",
            {
                "form": form,
                "post": post,
            },
        )


@permission_required(perm="root.view_root", raise_exception=True)
def post_details(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("root:root"))
    return render(
        request,
        "root/posts/post.html",
        {
            "post": post,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def user_details(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user is None:
        messages.error(request, "Usuario no encontrado")
        return redirect(reverse("root:users"))
    content = request.GET.get("content", "comments")
    comments = None
    questions = None
    if content == "comments":
        comments = Comment.objects.filter(author=user)
    elif content == "questions":
        questions = Question.objects.filter(author=user)
    else:
        messages.error(request, f"Opción {content} no es valida")
        return redirect(reverse("root:user_details", args=[user_id]))
    return render(
        request,
        "root/users/user.html",
        {
            "user_detail": user,
            "comments": comments,
            "questions": questions,
            "content": content,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def tag_details(request, tag_id):
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        messages.error(request, "Etiqueta no encontrado")
        return redirect(reverse("root:tags"))
    return render(
        request,
        "root/tags/tag.html",
        {"tag": tag, "posts_json": serialize("json", tag.posts.all())},
    )


@permission_required(perm="root.view_root", raise_exception=True)
def question_details(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("root:questions"))
    return render(
        request,
        "root/questions/question.html",
        {"question": question},
    )


@permission_required(perm="root.view_root", raise_exception=True)
def remove_question(request, user_id: int, question_id: int):
    question = Question.objects.filter(id=question_id).first()
    if question is None:
        messages.error(request, "Pregunta no encontrada")
        return redirect(reverse("questions:questions"))
    question.delete()
    return redirect(
        f"{reverse('root:user_details', args=[user_id])}?content=questions",
    )


@permission_required(perm="root.view_root", raise_exception=True)
def remove_comment(request, user_id: int, comment_id: int):
    comment = Comment.objects.filter(id=comment_id).first()
    if comment is None:
        messages.error(request, "Comentario no encontrado")
        return redirect(reverse("root:user_details", args=[user_id]))
    comment.delete()
    return redirect(reverse("root:user_details", args=[user_id]))
