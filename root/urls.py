"""
URL configuration for root project.

The `urlpatterns` list routes URLs to auth. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function auth
    1. Add an import:  from my_app import auth
    2. Add a URL to urlpatterns:  path('', auth.home, name='home')
Class-based auth
    1. Add an import:  from other_app.auth import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from root import custom_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView,
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('olcha/', include('app.urls')),
                  path('api-token-auth/', custom_token.CustomAuthToken.as_view()),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
