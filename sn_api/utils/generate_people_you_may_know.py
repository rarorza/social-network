import os
import sys

import django

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
django.setup()

from account.models import User


def generate_suggestions() -> None:
    users = User.objects.all()

    for user in users:
        user.people_you_may_know.clear()

        print("Find friends for: ", user)
        for friend in user.friends.all():
            print("Is friend with: ", friend)
            for friend_of_friend in friend.friends.all():
                if (
                    friend_of_friend not in user.friends.all()
                    and friend_of_friend != user
                ):
                    print("Suggest: ", friend_of_friend)
                    user.people_you_may_know.add(friend_of_friend)


if __name__ == "main":
    generate_suggestions()
