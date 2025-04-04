from celery import shared_task

from posts.models import Comment
from samer.detoxify import predict_detoxify


@shared_task
def detoxify_comments():
    comments = Comment.objects.filter(moderate=False)
    if comments.count() == 0:
        return
    data = [comment.text for comment in comments]
    detoxify_res = predict_detoxify(data)
    toxic = set(
        [t[0] for key in detoxify_res for t in detoxify_res[key]["info"]],
    )
    toxic_comments = list(
        filter(
            lambda c: c.text in toxic,
            comments,
        ),
    )
    toxic_ids = [q.id for q in toxic_comments]
    non_toxic_ids = [q.id for q in comments if q.id not in toxic_ids]
    Comment.objects.filter(
        id__in=toxic_ids,
    ).update(toxic=True, moderate=True)
    Comment.objects.filter(
        id__in=non_toxic_ids,
    ).update(moderate=True)
