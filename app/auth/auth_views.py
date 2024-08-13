# from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from app.serializers import LoginSerializer, RegisterSerializer
#
#
# class LoginApiView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             response = {
#                 'username': {
#                     'detail': 'Username does not exist',
#                 }
#             }
#             if User.objects.filter(username=serializer.data['username']).exists():
#                 user = User.objects.get(username=serializer.data['username'])
#                 # token = Token.objects.create(user)
#                 response = {
#                     'success': True,
#                     'username': user.username,
#                     # 'token': token.key,
#                     'email': user.email,
#                 }
#                 return Response(response, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LogoutApiView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#
#     def post(self, request, *args, **kwargs):
#         # token = Token.objects.get(user=request.user)
#         # token.delete()
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Successfully logged out.'
#             },
#             status=status.HTTP_200_OK)
#
# class RegisterApiView(APIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#
#     def post(self, serializer):
#         user = serializer.save()
#         token, _ = Token.objects.get(user=user)
#         self.token = token.key
#
#     def create(self, request, *args, **kwargs):
#         response=super().create(request, *args, **kwargs)
#         response.data['success'] = True
#         response.data['token'] = self.token
#         return Response
#


from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
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
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        return Response(
            {
                'success': True,
                'message': 'Successfully logged out.'
            },
            status=status.HTTP_200_OK)


class RegisterApiView(APIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            response = {
                'success': True,
                'username': user.username,
                'email': user.email,
                'token': token.key
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
