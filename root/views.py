from django.shortcuts import render

from posts.models import Post


def root(request):
    posts = Post.objects.all()
    # posts = [
    #     {
    #         "id": str(post["_id"]),
    #         "name": post["name"],
    #         "comments": mongo_comment.count(query={"post": str(post["_id"])}),
    #         "likes": post["likes"],
    #         "type": "imagen" if post["type"] == "image" else "video",
    #         "tags": ", ".join(
    #             [
    #                 tag["name"]
    #                 for tag in mongo_tag.find(
    #                     query={"posts": str(post["_id"])},
    #                 )
    #             ]
    #         ),
    #     }
    #     for post in posts_db
    # ]
    return render(
        request,
        "root/posts/posts.html",
        {
            "posts": posts,
        },
    )
