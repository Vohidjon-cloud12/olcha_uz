# Create your auth here.
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from app import permissions
from app.models import Category, Product, Group, Attribute
from app.serializers import CategorySerializer, ProductSerializer, GroupSerializer, ProductDetailSerializer, \
    ProductAttributeSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsOwnerIsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('group_slug')

        queryset = Product.objects.all()

        if category_slug and group_slug:
            queryset = queryset.filter(group__category__slug=category_slug, group__slug=group_slug)
        elif category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        elif group_slug:
            queryset = queryset.filter(group__slug=group_slug)

        return queryset


class ProductDetail(APIView):
    def get(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, group_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAttributeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAttributeSerializer
    lookup_field = 'slug'

# class PostApiView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerialazer
