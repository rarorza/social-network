# Generated by Django 5.0.3 on 2024-03-11 23:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0006_trend'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('type_of_notification', models.CharField(choices=[('new_friend_request', 'New friend request'), ('accepted_friend_request', 'Accepted friend request'), ('rejected_friend_request', 'Rejected friend request'), ('post_like', 'Post like'), ('post_comment', 'Post comment')], max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_notifications', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
