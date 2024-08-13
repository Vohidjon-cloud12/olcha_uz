from django.db.migrations import serializer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers import LoginSerializer, RegisterSerializer


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                'username': {
                    'detail': 'Username does not exist',
                }
            }
            if User.objects.filter(username=serializer.data['username']).exists():
                user = User.objects.get(username=serializer.data['username'])
                token = Token.objects.create(user)
                response = {
                    'success': True,
                    'username': user.username,
                    'token': token.key,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # token = Token.objects.get(user=request.user)
        # token.delete()
        return Response(
            {
                'success': True,
                'message': 'Successfully logged out.'
            },
            status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Successfully registered.',
                    'username': User.objects.get(username=serializer.validated_data['username']).username,
                    'token' : Token.objects.get(
                        user=User.objects.get(username=serializer.validated_data['username']).key
                    )

                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


