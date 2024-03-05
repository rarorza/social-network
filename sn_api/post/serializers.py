from account.serializers import UserSerializer
from rest_framework import serializers

from .models import Comment, Post, Trend


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
        )


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # to show created_by.name in front end

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "likes_count",
            "comments_count",
            "created_by",
            "created_at_formatted",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "likes_count",
            "comments_count",
            "created_by",
            "created_at_formatted",
            "comments",
        )


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ("id", "hashtag", "occurrences")
