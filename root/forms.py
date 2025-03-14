from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from posts.models import Post


class StaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            samer_staff = Group.objects.get(name="Samer Staff")
            user.groups.add(samer_staff)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input", "id": "username", "placeholder": " "}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "input", "id": "password1", "placeholder": " "}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input", "id": "password2", "placeholder": " "}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "input", "id": "email", "placeholder": " "}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "input", "id": "first_name", "placeholder": " "}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "input", "id": "last_name", "placeholder": " "}
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadPost(forms.Form):
    file = MultipleFileField(
        widget=MultipleFileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        )
    )
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )
    des = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input description-form",
                "id": "des",
                "placeholder": " ",
            }
        ),
    )


class CreateTag(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        )
    )
    name = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )

    ids = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "ids",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        ids = kwargs.pop("ids", "")
        init = kwargs.pop("init", False)
        super().__init__(*args, **kwargs)
        if init:
            self.fields["ids"].initial = ids


class EditPost(forms.Form):
    file = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "class": "image-form",
                "style": "display: none",
            }
        ),
    )
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input name-form",
                "id": "name",
                "placeholder": " ",
            }
        ),
    )
    des = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input description-form",
                "id": "des",
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        post: Post = kwargs.pop("post", None)
        super().__init__(*args, **kwargs)
        if post is not None:
            self.fields["des"].initial = post["description"]
            self.fields["name"].initial = post["name"]
