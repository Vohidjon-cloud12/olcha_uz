from django.urls import path

from app import views

urlpatterns = [
    path('app/', views.CategoriyList.as_view(), name='app')]