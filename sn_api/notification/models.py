import uuid

from account.models import User
from django.db import models
from post.models import Post


class Notification(models.Model):
    NEW_FRIEND_REQUEST = "new_friend_request"
    ACCEPTED_FRIEND_REQUEST = "accepted_friend_request"
    REJECTED_FRIEND_REQUEST = "rejected_friend_request"
    POST_LIKE = "post_like"
    POST_COMMENT = "post_comment"

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEW_FRIEND_REQUEST, "New friend request"),
        (ACCEPTED_FRIEND_REQUEST, "Accepted friend request"),
        (REJECTED_FRIEND_REQUEST, "Rejected friend request"),
        (POST_LIKE, "Post like"),
        (POST_COMMENT, "Post comment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        related_name="created_notifications",
        on_delete=models.CASCADE,
    )
    created_for = models.ForeignKey(
        User,
        related_name="received_notifications",
        on_delete=models.CASCADE,
    )
