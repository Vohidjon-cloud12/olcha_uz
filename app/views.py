from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Category



class CategoriyList(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        category_data = [
            {
                'title': category.title,
                'slug': category.slug,
                'image': category.image.url,

            }
            for category in Category.objects.all()]
        return Response(category_data)

