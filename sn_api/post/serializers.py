from account.serializers import UserSerializer
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # to show created_by.name in front end

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "likes_count",
            "created_by",
            "created_at_formatted",
        )
