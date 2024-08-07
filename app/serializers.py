from django.db.models import Avg
from rest_framework import serializers
from app.models import Category, Product, Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_avg_rating(self, products):
        avg_rating = products.comments.aggregate(avg=Avg('rating'))['avg']
        if not avg_rating:
            return 0
        elif avg_rating > 0:
            return round(avg_rating, 2)

    def get_is_liked(self, products):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if_liked = products.is_liked.filter(id=request.user.id).exists()
            return if_liked
        return False

    def get_image(self, products):
        request = self.context.get('request')
        try:
            image = products.images.get(is_primary=True)
            return request.build_absolute_uri(image.image.url)
        except products.images.model.DoesNotExist:
            return None

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'discounted_price', 'is_liked', 'avg_rating', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


