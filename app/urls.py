from django.urls import path
from django.views.decorators.cache import cache_page

from app import views
from app.auth import auth_views


urlpatterns = [
    # category urls
    path('category/', views.CategoryListApiView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('category-create/', views.CreateCategoryView.as_view(), name='category-create'),
    path('category/<slug:slug>/delete/', views.DeleteCategoryView.as_view(), name='category-delete'),
    path('category/<slug:slug>/update/', views.UpdateCategoryView.as_view(), name='category-update'),
    # product urls
    path('products/<slug:category_slug>/<slug:group_slug>/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='pro0duct-detail'),
    # group  urls
    path('group-list/', views.GroupListView.as_view(), name='group-list'),
    path('group/<slug:slug>/', views.GroupDetailApiView.as_view(), name='group-detail'),
    path('attributes/<slug:slug>/', cache_page(60*5)(views.ProductAttributeView.as_view()), name='product-attributes'),
    # auth View
    path('login-page/', auth_views.LoginApiView.as_view()),
    path('logout-page/', auth_views.LogoutApiView.as_view()),
    path('register-page/', auth_views.RegisterApiView.as_view())
]
