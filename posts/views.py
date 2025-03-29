import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from posts.forms import CreateCommentForm
from posts.models import Comment, Post, Tag


def add_remove_like(request, post_id):
    allows_redirects = [
        "home:home_images",
        "home:home_videos",
        "posts:comment",
    ]
    redirect_view = request.GET.get("redirect", "home:home_images")
    post_type = None
    if redirect_view not in allows_redirects:
        messages.error(request, f"Redirección {redirect_view} no permitida")
    if redirect_view == "posts:comment":
        post_type: str = request.GET.get("type", "")
        if post_type == "" or post_type not in ["image", "video"]:
            messages.error(request, "Tipo de publicación incorrecto")
            return redirect(reverse("home:home_images"))
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        if post_type:
            return redirect(reverse(redirect_view, args=[post_id, post_type]))
        return redirect(reverse(redirect_view))
    if not request.user.is_authenticated:
        messages.warning(
            request,
            "Tienes tener una cuenta para dar un me gusta",
        )
        if post_type:
            return redirect(reverse(redirect_view, args=[post_id, post_type]))
        return redirect(reverse(redirect_view))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    if post_type:
        return redirect(reverse(redirect_view, args=[post_id, post_type]))
    return redirect(reverse(redirect_view))


def comments(request, post_id, post_type):
    template = ""
    if post_type == "IM":
        template = "posts/image.html"
    elif post_type == "VD":
        template = "posts/video.html"
    else:
        messages.error(request, "Tipo de publicación incorrecto")
        return redirect(reverse("home:home_images"))
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        if post_type == "VD":
            return redirect(reverse("home:home_videos"))
        else:
            return redirect(reverse("home:home_images"))
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Hay que tener una sesión creada e iniciada",
            )
            return redirect(
                reverse(
                    "posts:comment",
                    args=[post_id, post_type],
                )
            )
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["comment"]
            Comment.objects.create(
                text=comment,
                post=post,
                author=request.user,
            )
    comment_form = CreateCommentForm()
    comments = Comment.objects.filter(post=post, toxic=False)
    return render(
        request,
        template,
        {
            "post": post,
            "comments": comments,
            "form": comment_form,
        },
    )


def remove_comment(request, post_id: int, comment_id: int):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        messages.error(request, "Publicación no encontrada")
        return redirect(reverse("home:home_videos"))
    post_type = post.sources.first().type
    comment = Comment.objects.filter(id=comment_id).first()
    if comment is None:
        messages.error(request, "Comentario no encontrado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_type]),
        )
    if not comment.author == request.user:
        messages.error(request, "El comentario no puede ser eliminado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_type]),
        )
    comment.delete()
    comment_form = CreateCommentForm()
    comments = Comment.objects.filter(post=post, toxic=False)
    template = "posts/image.html"
    mime_types = [source.get_mime_type() for source in post.sources]
    if post_type == "video":
        template = "posts/video.html"
    return render(
        request,
        template,
        {
            "post": post,
            "mime_types": mime_types,
            "comments": comments,
            "form": comment_form,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def add_post_to_tag(request, tag_id: str):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_ids = data.get("post_ids", [])
            tag = Tag.objects.filter(id=tag_id).first()
            if tag is None:
                messages.error(request, "Etiqueta no encontrada")
                return redirect(reverse("root:tags"))
            posts = Post.objects.filter(id__in=post_ids)
            tag.posts.add(*posts)
            return redirect(reverse("root:tag_details", args=[tag_id]))
        except ValueError:
            messages.warning(request, "Invalid JSON data")
            return redirect(reverse("root:tags"))


@permission_required(perm="root.view_root", raise_exception=True)
def search_posts(request):
    post_name = request.GET.get("post_name", "")
    if post_name == "":
        return JsonResponse([], safe=False)
    posts = list(Post.objects.filter(name__icontains=post_name))
    return JsonResponse(posts, safe=False)
