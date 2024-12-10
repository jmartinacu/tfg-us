from django.shortcuts import redirect, render
from django.urls import reverse

from posts.forms import CreateCommentForm
from posts.models import Comment, Post


def add_remove_like(request, post_id):
    # allows_redirects = [
    #     "home:home_images",
    #     "home:home_videos",
    #     "posts:comment",
    # ]
    redirect_view = request.GET.get("redirect", "home:home_images")
    post_type = None
    # if redirect_view not in allows_redirects:
    # TODO: ADD messages.error(request, f"Redirección {redirect_view} no permitida")
    if redirect_view == "posts:comment":
        post_type: str = request.GET.get("type", "")
        if post_type == "" or post_type not in ["image", "video"]:
            # TODO: ADD messages.error(request, "Tipo de publicación incorrecto")
            return redirect(reverse("home:home_images"))
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        # TODO: messages.error(request, "Publicación no encontrada")
        if post_type:
            return redirect(reverse(redirect_view, args=[post_id, post_type]))
        return redirect(reverse(redirect_view))
    if not request.user.is_authenticated:
        # TODO: ADD messages.warning(
        #     request,
        #     "Tienes tener una cuenta para dar un me gusta",
        # )
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
        # TODO: messages.error(request, "Tipo de publicación incorrecto")
        return redirect(reverse("home:home_images"))
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        # TODO: messages.error(request, "Publicación no encontrada")
        if post_type == "VD":
            return redirect(reverse("home:home_videos"))
        else:
            return redirect(reverse("home:home_images"))
    if request.method == "POST":
        if not request.user.is_authenticated:
            # TODO: messages.error(
            #     request,
            #     "Hay que tener una sesión creada e iniciada",
            # )
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
    mime_types = [source.get_mime_type() for source in post.sources]
    comment_form = CreateCommentForm()
    comments = Comment.objects.filter(post=post)
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


def remove_comment(request, post_id: str, comment_id: str):
    post = Post.objects.filter(id=post_id).first()
    if post is None:
        # TODO: messages.error(request, "Publicación no encontrada")
        return redirect(reverse("home:home_videos"))
    post_type = post.post_type
    comment = Comment.objects.filter(id=comment_id).first()
    if comment is None:
        # TODO: messages.error(request, "Comentario no encontrado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_type]),
        )
    if not comment.author == request.user:
        # TODO: messages.error(request, "El comentario no puede ser eliminado")
        return redirect(
            reverse("posts:comment", args=[post_id, post_type]),
        )
    comment.delete()
    comment_form = CreateCommentForm()
    comments = Comment.objects.filter(post=post)
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
