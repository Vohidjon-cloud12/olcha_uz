from django.urls import path

from app import views
urlpatterns = [
    path('categories/',views.CategoryListApiView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('category-create/', views.CreateCategoryView.as_view(), name='category-create'),
    path('category/<slug:slug>/delete/', views.DeleteCategoryView.as_view(), name='category-delete'),
    path('category/<slug:slug>/update/', views.UpdateCategoryView.as_view(), name='category-update'),

    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    # Group urls
    path('group-list/', views.GroupListView.as_view(), name='group-list'),
    path('group/<slug:slug>/', views.GroupDetailApiView.as_view(), name='group-detail'),
    ]

