from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        user.is_staff = True
        if commit:
            user.save()
        return user


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
