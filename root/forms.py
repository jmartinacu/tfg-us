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
