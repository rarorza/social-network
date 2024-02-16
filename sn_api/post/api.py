from account.models import User
from account.serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def post_list(request):
    posts = Post.objects.all()
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
