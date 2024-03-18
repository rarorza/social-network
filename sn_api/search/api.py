from account.models import User
from account.serializers import UserSerializer
from django.db.models import Q
from django.http import JsonResponse
from post.models import Post
from post.serializers import PostSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["POST"])
def search(request):
    data = request.data
    query = data["query"]

    friends_ids = [request.user.id]
    for friend in request.user.friends.all():
        friends_ids.append(friend.id)

    if len(query) >= 2:
        users = User.objects.filter(name__icontains=query)
        users_serializer = UserSerializer(users, many=True)

        posts = Post.objects.filter(
            Q(body__icontains=query, is_private=False)
            | Q(created_by_id__in=list(friends_ids), body__icontains=query)
        )
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(
            {"users": users_serializer.data, "posts": posts_serializer.data},
            safe=False,
        )
    return JsonResponse({"error": "query length < 2"}, status=400)
