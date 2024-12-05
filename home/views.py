from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse

from home.forms import ProfileForm
from home.models import ProfileInformation
from posts.models import Post
from samer.bucket import delete_file, upload_file


def home_images(request):
    posts = Post.objects.filter(
        post_type=Post.PostTypes.IMAGE,
    ).annotate(
        comments=Count("comments"),
    )
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )


def home_videos(request):
    posts = Post.objects.filter(
        post_type=Post.PostTypes.VIDEO,
    ).annotate(
        comments=Count("comments"),
    )
    return render(
        request,
        "home/home.html",
        {
            "posts": posts,
        },
    )


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
