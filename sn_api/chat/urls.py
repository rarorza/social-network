from django.urls import path

from . import api

urlpatterns = [
    path("", api.conversation_list, name="conversation_list"),
    path(
        "<uuid:conversation_id>/",
        api.conversation_detail,
        name="conversation_detail",
    ),
    path(
        "send/<uuid:conversation_id>/",
        api.conversation_send_message,
        name="conversation_send_message",
    ),
    path(
        "get-or-create/<uuid:user_id>/",
        api.conversation_get_or_create,
        name="conversation_get_or_create",
    ),
]
