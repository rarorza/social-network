from django.urls import path

from . import api

urlpatterns = [
    path("", api.post_list, name="post_list"),
    path("<uuid:id>/", api.post_detail, name="post_detail"),
    path("like/<uuid:id>/", api.post_like, name="post_like"),
    path(
        "comment/<uuid:id>/",
        api.post_create_comment,
        name="post_create_comment",
    ),
    path("profile/<uuid:id>/", api.post_list_profile, name="post_list_profile"),
    path("create/", api.post_create, name="post_create"),
]
