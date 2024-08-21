from django.db.models import Avg
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token

from app.models import Category, Product, Group, Attribute,Comment


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
    user_like = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_avg_rating(self, products):
        avg_rating = products.comments.aggregate(avg=Avg('rating'))['avg']
        if not avg_rating:
            return 0
        elif avg_rating > 0:
            return round(avg_rating, 2)

    def get_user_like(self, products):
        request = self.context.get('request')
        if request.user.is_authenticated:
            user_like = products.user_like.filter(id=request.user.id).exists()
            return user_like
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
        fields = ['id', 'name', 'price', 'discount', 'discounted_price', 'user_like', 'avg_rating', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    password2 = serializers.CharField(max_length=100, required=True, write_only=True)
    email = serializers.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
