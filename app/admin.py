from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image']