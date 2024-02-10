from django.http import JsonResponse
from rest_framework.decorators import api_view
from serializers import PostSerializer

from .models import Post


@api_view(["GET"])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse({"data": serializer.data})
