from django import forms


class CreateQuestionForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input title-form",
                "id": "title",
                "placeholder": " ",
            }
        ),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "input content-form",
                "id": "content",
                "placeholder": " ",
                "style": "resize: none;",
            }
        ),
    )

    tags = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "input tag-form",
                "id": "tag",
            }
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        title = kwargs.pop("title", None)
        content = kwargs.pop("content", None)
        super().__init__(*args, **kwargs)
        if title is not None:
            self.fields["title"].initial = title
        if content is not None:
            self.fields["content"].initial = content


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

    def __init__(self, *args, **kwargs) -> None:
        question = kwargs.pop("question", "")
        super().__init__(*args, **kwargs)
        self.fields["question"].initial = question
