from django.db.models import Avg
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token

from app.models import Category, Product, Group, Attribute


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


#
# class ProductAttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'slug','get_attributes']

# class Meta:
#     model = Category
#     fields = '__all__'
class ProductAttributeSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, products):
        attributes = Attribute.objects.filter(product=products.id)
        attributes_dict = {}
        for attribute in attributes:
            attributes_dict[attribute.key.name] = attribute.value.name
        return attributes_dict

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'attributes']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=True)
    password2 = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=100, required=True)

    class Meta:

        model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')


    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        return username


    def validate(self, instance):
        if instance.password != instance.password2:
            data = {
                'error': 'Passwords do not match',
            }
            raise serializers.ValidationError(data)

        if User.objects.filter(email=instance['email']).exists():
            raise serializers.ValidationError('Email already registered')

        return instance


    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
