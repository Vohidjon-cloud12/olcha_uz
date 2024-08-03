from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)

        super(Category,self).save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Group, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    user_likes = models.ManyToManyField(User)


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=100)

    def __str__(self):
        return self.key_name

class AttributeValue(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

class Attribute(models.Model):
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    rating = models.IntegerField(default=0)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)