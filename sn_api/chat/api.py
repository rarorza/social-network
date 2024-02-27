from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import (
    ConversationDetailSerializer,
    ConversationMessageSerializer,
    ConversationSerializer,
)


@api_view(["GET"])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def conversation_detail(request, id):
    conversation = Conversation.objects.filter(
        users__in=list([request.user])  # noqa 501
    ).get(pk=id)
    serializer = ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def conversation_send_message(request, id):
    conversation = Conversation.objects.filter(
        users__in=list([request.user])  # noqa 501
    ).get(pk=id)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get("body"),
        created_by=request.user,
        sent_to=sent_to,
    )
    serializer = ConversationMessageSerializer(conversation_message)
    return JsonResponse(serializer.data, safe=False)
