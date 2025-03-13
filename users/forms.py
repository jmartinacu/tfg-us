from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input", "id": "user", "placeholder": " "}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input", "id": "password", "placeholder": " "}
        )


class SigninForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input", "id": "user", "placeholder": " "}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "input", "id": "password1", "placeholder": " "}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input", "id": "password2", "placeholder": " "}
        )


class AdminSiginForm(forms.Form):
    user = forms.CharField(label="Nombre de usuario")
    pwd = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    email = forms.EmailField(label="Correo electronico")
    name = forms.CharField(label="Nombre")
    surname = forms.CharField(label="Apellido")
