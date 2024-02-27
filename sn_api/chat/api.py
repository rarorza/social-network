from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import (
    ConversationMessage,
    ConversationMessageSerializer,
    ConversationSerializer,
)


@api_view(["GET"])
def conversation_list(request):
    return JsonResponse({"msg": "conversation"})
