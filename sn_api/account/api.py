from account.models import FriendshipResquest, User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from notification.utils.notifications import create_notification
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from .forms import ProfileForm, SignupForm
from .serializers import FriendshipResquestSerializer, UserSerializer


@api_view(["GET"])
def me(request):
    return JsonResponse(
        {
            "id": request.user.id,
            "name": request.user.name,
            "email": request.user.email,
            "avatar": request.user.get_avatar(),
        }
    )


@api_view(["POST"])
def profile_edit(request):
    user = request.user
    email = request.data.get("email")
    email_already_exists = User.objects.exclude(id=user.id).filter(email=email).exists()

    if email_already_exists:
        return JsonResponse({"message": "Email already exists"})
    else:
        print(request.FILES)
        print(request.POST)
        form = ProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=user,
        )

        if form.is_valid():
            user.save()

        serializer = UserSerializer(user)
        return JsonResponse(
            {
                "message": "Information updated",
                "user": serializer.data,
            }
        )


@api_view(["POST"])
def password_edit(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
        return JsonResponse({"message": "success"})
    errors = form.errors.as_json()
    return JsonResponse({"message": errors}, safe=False)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    messages = "success"

    form = SignupForm(
        {
            "email": data.get("email"),
            "name": data.get("name"),
            "password1": data.get("password1"),
            "password2": data.get("password2"),
        }
    )

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()
        print(user.id, user.email)

        url = f"http://127.0.0.1:8000/api/activate_email/?email={user.email}&id={user.id}"  # noqa 501

        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "noreply@sn.com",
            [user.email],
            fail_silently=False,
        )
    else:
        messages = form.errors.as_json()
    return JsonResponse({"message": messages}, safe=False)


@api_view(["GET"])
def friends(request, id):
    user = User.objects.get(pk=id)
    friendship_requests = []

    if user == request.user:
        friendship_requests = FriendshipResquest.objects.filter(
            created_for=request.user, status=FriendshipResquest.SENT
        )
    friends = user.friends.all()

    user_serializer = UserSerializer(user)
    friends_serializer = UserSerializer(friends, many=True)
    friendship_requests_serializer = FriendshipResquestSerializer(
        friendship_requests,
        many=True,
    )

    return JsonResponse(
        {
            "user": user_serializer.data,
            "friends": friends_serializer.data,
            "requests": friendship_requests_serializer.data,
        },
        safe=False,
    )


@api_view(["POST"])
def send_friendship_request(request, id):
    user_receiver = User.objects.get(pk=id)
    user_sender = request.user

    check_invite_from_receiver = FriendshipResquest.objects.filter(
        created_for=user_receiver
    ).filter(created_by=user_sender)

    check_invite_from_sender = FriendshipResquest.objects.filter(
        created_for=user_sender
    ).filter(created_by=user_receiver)

    if not check_invite_from_receiver or not check_invite_from_sender:
        friendship_request = FriendshipResquest.objects.create(
            created_for=user_receiver,
            created_by=user_sender,
        )

        create_notification(
            request,
            "new_friend_request",
            friend_request_id=friendship_request.id,
        )

        return JsonResponse({"message": "friendship request created"})
    return JsonResponse({"message": "request already sent"})


@api_view(["POST"])
def handle_friendship_request(request, id, status):
    user_sent = User.objects.get(pk=id)
    user_receive = request.user

    friendship_request = FriendshipResquest.objects.filter(
        created_for=user_receive
    ).get(created_by=user_sent)
    friendship_request.status = status
    friendship_request.save()

    if friendship_request.status == "accepted":
        user_sent.friends.add(user_receive)
        user_sent.friends_count += 1
        user_sent.save()

        user_receive.friends.add(user_sent)
        user_receive.friends_count += 1
        user_receive.save()
        create_notification(
            request,
            "accepted_friend_request",
            friend_request_id=friendship_request.id,
        )
    elif friendship_request.status == "rejected":
        create_notification(
            request,
            "rejected_friend_request",
            friend_request_id=friendship_request.id,
        )

    return JsonResponse({"message": "friendship request updated"})
