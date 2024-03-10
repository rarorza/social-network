from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path("me/", api.me, name="me"),
    path("signup/", api.signup, name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/edit/", api.profile_edit, name="profile_edit"),
    path("profile/edit/password/", api.password_edit, name="password_edit"),
    path("friends/<uuid:id>/", api.friends, name="friends"),
    path(
        "friends/<uuid:id>/request/",
        api.send_friendship_request,
        name="send_friendship_request",
    ),
    path(
        "friends/<uuid:id>/<str:status>/",
        api.handle_friendship_request,
        name="handle_request",
    ),
]
