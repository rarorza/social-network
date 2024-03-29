import uuid
from typing import Type

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    """
    Methods override to make user creation with email mandatory
    """

    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail-address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staf", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(
        self, name=None, email=None, password=None, **extra_fields
    ):  # noqa 501
        extra_fields.setdefault("is_staf", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    friends = models.ManyToManyField("self")
    friends_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    people_you_may_know = models.ManyToManyField("self")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    data_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()  # override the default manager

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_avatar(self) -> str | None:
        if self.avatar:
            return "http://127.0.0.1:8000" + self.avatar.url
        return "http://127.0.0.1:8000/media/avatars/placeholder_user.jpg"


class FriendshipRequest(models.Model):
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (SENT, "Sent"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="created_friendship_request",
        on_delete=models.CASCADE,
    )
    created_for = models.ForeignKey(
        User,
        related_name="received_friendship_request",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=SENT,
    )

    @classmethod
    def can_send_friend_request(
        cls, user_visitor: Type[User], user_guest: Type[User]
    ) -> bool:
        can_send = True

        check_invite_from_visitor = FriendshipRequest.objects.filter(
            created_for=user_visitor
        ).filter(created_by=user_guest)
        check_invite_from_guest = FriendshipRequest.objects.filter(
            created_for=user_guest
        ).filter(created_by=user_visitor)

        if (
            check_invite_from_visitor
            or check_invite_from_guest
            or user_visitor in user_guest.friends.all()
        ):
            can_send = False
        return can_send
