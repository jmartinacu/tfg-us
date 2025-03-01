from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from home.forms import ProfileForm
from home.models import ProfileInformation
from posts.models import FilesTypes, Post, Tag
from samer.bucket import delete_file, upload_file


def home_images(request):
    posts = Post.objects.filter(
        sources__type=FilesTypes.IMAGE,
    ).distinct()
    tags = Tag.objects.all()
    profile = ProfileInformation.objects.first()
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
            "profile": profile,
            "tags": tags,
        },
    )


def home_videos(request):
    posts = Post.objects.filter(
        sources__type=FilesTypes.VIDEO,
    ).distinct()
    profile = ProfileInformation.objects.first()
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
            "profile": profile,
        },
    )


@permission_required(perm="root.view_root", raise_exception=True)
def home_edit_profile(request):
    profile = ProfileInformation.objects.first()
    if request.method == "POST" and "image_url" in request.FILES:
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            app_name = profile_form.cleaned_data["app_name"]
            app_real_name = profile_form.cleaned_data["app_real_name"]
            descriptions = profile_form.cleaned_data["descriptions"]
            url = profile_form.cleaned_data["url"]
            new_image = profile_form.cleaned_data["image_url"]
            new_image_name = str(new_image.name)
            profile_image_name = profile.image_url.split("/")[-1]
            delete_file(profile_image_name)
            uploaded_file_url = upload_file(
                new_image,
                object_name=new_image_name,
            )
            profile.delete()
            ProfileInformation.objects.create(
                app_name,
                app_real_name,
                descriptions=descriptions.splitlines(),
                image_url=uploaded_file_url,
                url=url,
            )
            return redirect(reverse("home:home_images"))
    else:
        profile_form = ProfileForm()
        return render(
            request,
            "home/profile.html",
            {
                "profile": profile,
                "form": profile_form,
            },
        )


def add_message(request):
    level_msg = request.GET.get("level", "info")
    message = request.GET.get("message", "")
    if message == "":
        return JsonResponse(
            {"status": "error", "msg": "Message mandatory"},
            status=400,
        )
    level = messages.INFO
    if level_msg == "success":
        level = messages.SUCCESS
    if level_msg == "warning":
        level = messages.WARNING
    if level_msg == "error":
        level = messages.ERROR
    messages.add_message(request, level, message)
    return JsonResponse({"status": "ok"})


def home_tag(request, tag_id: str):
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        return redirect(reverse("home:home_images"))
    tags = Tag.objects.all()
    profile = ProfileInformation.objects.first()
    return render(
        request,
        "home/home.html",
        {
            "profile": profile,
            "posts": tag.posts,
            "tags": tags,
        },
    )
