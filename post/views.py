from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post
from post.serializers import PostSerializer


# Create your views here.

class PostApiView(APIView, PageNumberPagination):
    pass


class PostDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        cache_key = f'post_detail_{post_id}'
        post_data = cache.get(cache_key)
        if post_data is None:
            post_data = Post.objects.get(id=post_id)
            serializer = PostSerializer(post_data, many=False)
            cache.set(cache_key, serializer, timeout=300)
            return Response(serializer, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
