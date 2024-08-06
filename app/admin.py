from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Product, Group, AttributeKey, AttributeValue, Comment, Image


# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image']
    list_display = ['title', 'image', 'slug']
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'group', 'discount']
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ['name', 'image', 'category']
    list_display = ['name', 'image', 'category']
    search_fields = ['name']
    list_filter = ['category']


@admin.register(AttributeKey)
class GroupAdmin(admin.ModelAdmin):
    fields = ['key_name', ]


@admin.register(AttributeValue)
class GroupAdmin(admin.ModelAdmin):
    fields = ['value']


@admin.register(Comment)
class GroupAdmin(admin.ModelAdmin):
    fields = ['comment']



@admin.register(Image)
class GroupAdmin(admin.ModelAdmin):
    fields = ['image']
    list_display = ['image']
