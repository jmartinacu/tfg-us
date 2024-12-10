from django.shortcuts import render

from questions.models import Question


def questions(request):
    option = request.GET.get("option", "")
    search = request.GET.get("search", "")
    if option == "author":
        query = {"author__username__startswith": search}
    elif option == "content":
        query = {"content__icontains": search}
    elif option == "title":
        query = {"title__startswith": search}
    elif option == "tag":
        query = {"tags__in": search.split(",")}
    elif option == "resolved":
        query = {"resolve": True}
    else:
        query = {}
    questions = Question.objects.filter(**query)
    return render(
        request,
        "questions/questions_content.html",
        {"questions": questions},
    )
