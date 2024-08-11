from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import Category, Product, Group, AttributeKey, AttributeValue, Comment, Image


# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'get_image']
    list_display = ['title', 'get_image', 'slug']
    search_fields = ['title']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50' height='50'>")

    get_image.short_description = 'Image'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'group', 'discount', 'user_like']

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


class CommentAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product', 'user',]
    readonly_fields = ['user']  # Optionally make the user field read-only

    def save_model(self, request, obj, form, change):
        if not change:  # Only set user on creation, not on updates
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Comment, CommentAdmin)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['is_primary', 'image', 'product']
