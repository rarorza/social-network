import os
import sys
from collections import Counter
from datetime import timedelta

import django
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
django.setup()
from post.models import Post, Trend


def extract_hashtags(text: str, trends: list) -> list:
    for word in text.split():
        if word[0] == "#":
            trends.append(word[1:])
    return trends


def generate_trends() -> None:
    for trend in Trend.objects.all():
        trend.delete()

    trends = []
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    twenty_for_hours = this_hour - timedelta(hours=24)
    posts = Post.objects.filter(created_at__gte=twenty_for_hours).filter(
        is_private=False
    )

    for post in posts:
        extract_hashtags(post.body, trends)

    for trend in Counter(trends).most_common(10):
        Trend.objects.create(hashtag=trend[0], occurrences=trend[1])


if __name__ == "__main__":
    generate_trends()
