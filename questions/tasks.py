from celery import shared_task

from questions.models import Question
from samer.detox import predict_detoxify


@shared_task
def detoxify_questions():
    questions = Question.objects.filter(moderate=False)
    if questions.count() == 0:
        return
    data = []
    for question in questions:
        data.append(question.title)
        data.append(question.content)
    detoxify_res = predict_detoxify(data)
    toxic = set(
        [t[0] for key in detoxify_res for t in detoxify_res[key]["info"]],
    )
    toxic_questions = list(
        filter(
            lambda q: q.title in toxic or q.content in toxic,
            questions,
        ),
    )
    toxic_ids = [q.id for q in toxic_questions]
    non_toxic_questions = [q for q in questions if q.id not in toxic_ids]
    Question.objects.filter(
        id__in=toxic_ids,
    ).update(toxic=True, moderate=True)
    Question.objects.filter(
        id__in=[q.id for q in non_toxic_questions],
    ).update(moderate=True)
