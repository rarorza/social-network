# Generated by Django 5.0.2 on 2024-02-27 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_comments_count_comment_post_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]
