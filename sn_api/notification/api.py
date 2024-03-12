from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Notification
from .serializers import NotificationSerializer


@api_view(["GET"])
def notifications(request):
    user = request.user
    received_notifications = user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)
    return JsonResponse(serializer.data, safe=False)
