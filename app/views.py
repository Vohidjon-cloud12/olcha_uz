# Create your auth here.
from django.core.cache import cache
from django.db.models import Avg, Prefetch
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from app import permissions
from app.models import Category, Product, Group, Attribute, Image, Comment
from app.serializers import CategorySerializer, ProductSerializer, GroupSerializer, ProductDetailSerializer, \
    ProductAttributeSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    # @cache_page(60)
    # @method_decorator(cache_page(60))
    # def get(self, request, *args, **kwargs):
    #     return super().get(*args, **kwargs)
    #
    # def get_queryset(self):
    #     queryset = Category.objects.select_related('group').prefetch_related('products')

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)


class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_object(self):
        obj = get_object_or_404(Group, slug=self.kwargs['slug'])
        if not obj:
            raise NotFound("Group not found")
        return obj


class GroupDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'slug'


# /auth of products
# class ProductList(APIView):
#     def get(self, request, category_slug, group_slug):
#         products = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsOwnerIsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('slug')

        cache_key = f'product_list_{category_slug}_{group_slug}'
        cached_queryset = cache.get(cache_key)
        # Use select_related for foreign keys and prefetch_related for many-to-many and reverse relationships

        if cached_queryset is not None:
            return cached_queryset

        queryset = Product.objects.select_related('group__category').prefetch_related(
            Prefetch('images', queryset=Image.objects.filter(is_primary=True)),
            Prefetch('comments', queryset=Comment.objects.all()),
            'user_like'
        ).annotate(avg_rating=Avg('comments__rating'))

        if category_slug and group_slug:
            queryset = queryset.filter(group__category__slug=category_slug, group__slug=group_slug)
        elif category_slug:
            queryset = queryset.filter(group__category__slug=category_slug)
        elif group_slug:
            queryset = queryset.filter(group__slug=group_slug)
        cache.set(cache_key, queryset, 60 * 5)
        return queryset



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.all().prefetch_related('images', 'comments').annotate(avg_rating=Avg('comments__rating'))

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        cache_key = f'product_detail_{slug}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)
        product = self.get_object()
        serializer = self.get_serializer(product)
        data = serializer.data
        cache.set(cache_key, data, timeout=60*5)

        return Response(data, status=status.HTTP_200_OK)


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.select_related('category')
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_object(self):
        obj = get_object_or_404(Group, slug=self.kwargs['slug'])
        if not obj:
            raise NotFound("Group not found")
        return obj



class ProductAttributeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAttributeSerializer
    lookup_field = 'slug'

# class PostApiView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerialazer
