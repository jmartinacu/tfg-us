from django import forms


class CreateQuestionAnswerForm(forms.Form):

    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input question-form",
                "id": "question",
                "placeholder": " ",
            }
        ),
    )

    answer = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input answer-form",
                "id": "answer",
                "placeholder": " ",
            }
        ),
    )

    admin = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "input author-form",
                "id": "author",
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        admin_username = kwargs.pop("admin", None)
        question = kwargs.pop("question", "")
        super().__init__(*args, **kwargs)
        self.fields["question"].initial = question
        if admin_username is not None:
            self.fields["admin"].initial = admin_username
