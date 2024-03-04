from rest_framework import serializers

from .models import FriendshipResquest, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "friends_count", "posts_count")


class FriendshipResquestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # This makes 'created_by' return fields only from the 'UserSerializer'

    class Meta:
        model = FriendshipResquest
        fields = ("id", "created_by")
