from account.models import User
from account.serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .forms import PostForm
from .models import Like, Post
from .serializers import PostSerializer


@api_view(["GET"])
def post_list(request):
    user = request.user
    feed_users_ids = [user.id]

    for friend in request.user.friends.all():
        feed_users_ids.append(friend.id)

    posts = Post.objects.filter(created_by_id__in=list(feed_users_ids))
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serialize = UserSerializer(user)

    return JsonResponse(
        {"posts": posts_serializer.data, "user": user_serialize.data},
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    form = PostForm(request.data)
    print(request)

    if form.is_valid():
        # Commit is False because we need to delay for attach the user in form
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse(serializer.errors, status=400)


@api_view(["POST"])
def post_like(request, id):
    post = Post.objects.get(pk=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post.likes_count += 1
        post.likes.add(like)
        post.save()
        return JsonResponse({"message": "like created"})
    return JsonResponse({"message": "post already liked"})
