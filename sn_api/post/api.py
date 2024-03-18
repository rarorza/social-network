from account.models import User
from account.serializers import UserSerializer
from django.db.models import Q
from django.http import JsonResponse
from notification.utils.notifications import create_notification
from rest_framework.decorators import api_view
from utils.generate_trends import generate_trends

from .forms import AttachmentForm, PostForm
from .models import Comment, Like, Post, Trend
from .serializers import (
    CommentSerializer,
    PostDetailSerializer,
    PostSerializer,
    TrendSerializer,
)


@api_view(["GET"])
def post_list(request):
    user = request.user
    feed_users_ids = [user.id]

    for friend in request.user.friends.all():
        feed_users_ids.append(friend.id)

    trend = request.GET.get("trend", "")
    if trend:
        posts = Post.objects.filter(body__icontains="#" + trend).filter(
            is_private=False
        )
    else:
        posts = Post.objects.filter(created_by_id__in=list(feed_users_ids))
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_detail(request, id):
    user = request.user
    users_ids = [user.id]

    for friend in request.user.friends.all():
        users_ids.append(friend.id)

    post = Post.objects.filter(
        Q(created_by_id__in=list(users_ids)) | Q(is_private=False)
    ).get(pk=id)
    post_serializer = PostDetailSerializer(post)
    return JsonResponse({"post": post_serializer.data})


@api_view(["GET"])
def post_list_profile(request, id):
    user_profile = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if request.user not in user_profile.friends.all():
        posts = Post.objects.filter(created_by_id=id).filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serialize = UserSerializer(user_profile)

    return JsonResponse(
        {
            "posts": posts_serializer.data,
            "user": user_serialize.data,
        },
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    form_post = PostForm(request.POST)
    form_attachment = AttachmentForm(request.POST, request.FILES)
    attachment = None

    if form_attachment.is_valid():
        print("attachment is valid")
        attachment = form_attachment.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form_post.is_valid():
        # Commit is False because we need to delay for attach the user in form
        post = form_post.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = post.created_by
        user.posts_count += 1
        user.save()

        serializer = PostSerializer(post)
        generate_trends()
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

        create_notification(request, "post_like", post.id)
        return JsonResponse({"message": "like created"})
    return JsonResponse({"message": "post already liked"})


@api_view(["POST"])
def post_create_comment(request, id):

    comment = Comment.objects.create(
        body=request.data.get("body"),
        created_by=request.user,
    )

    post = Post.objects.get(pk=id)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    create_notification(request, "post_comment", post.id)

    comment_serializer = CommentSerializer(comment)
    return JsonResponse(comment_serializer.data, safe=False)


@api_view(["GET"])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)
    return JsonResponse(serializer.data, safe=False)
