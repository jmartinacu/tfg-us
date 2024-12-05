from django.shortcuts import redirect
from django.urls import reverse

from posts.models import Post


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
