from typing import Type

from account.models import FriendshipResquest
from notification.models import Notification
from post.models import Post


def create_notification(
    request, type_of_notification, post_id=None, friend_request_id=None
) -> Type[Notification]:
    created_for = None

    if type_of_notification == "post_like":
        body = f"{request.user.name} liked one of your posts!"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == "post_comment":
        body = f"{request.user.name} commented on one of your posts!"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == "new_friend_request":
        frend_request = FriendshipResquest.objects.get(pk=friend_request_id)
        created_for = frend_request.created_for
        body = f"{request.user.name} send you a friend request!"
    elif type_of_notification == "accepted_friend_request":
        frend_request = FriendshipResquest.objects.get(pk=friend_request_id)
        created_for = frend_request.created_for
        body = f"{request.user.name} accepted your friend request!"
    elif type_of_notification == "rejected_friend_request":
        frend_request = FriendshipResquest.objects.get(pk=friend_request_id)
        created_for = frend_request.created_for
        body = f"{request.user.name} rejected your friend request!"

    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for,
    )

    return notification
