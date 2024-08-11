from typing import Any
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
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
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    user_like = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    @property
    def discounted_price(self) -> Any:
        if self.discount > 0:
            return self.price*(1-(self.discount/100))
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Product, self).save(*args, **kwargs)

    def get_attribute(self):
        product_attribute = Attribute.objects.filter(product=self)
        attributes = []
        for product_attribute in product_attribute:
            attributes.append({
                'attribute_key': product_attribute.key,
                'attribute_value': product_attribute.value
            })
        return attributes

    @property
    def get_attributes_as_dict(self) -> dict:
        attributes = self.get_attribute()
        attributes_dictionary = {}
        for attribute in attributes:
            attributes_dictionary[attribute['attribute_key']] = attribute['attribute_value']

        return attributes_dictionary


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
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    message = models.TextField()
    rating = models.IntegerField(choices=Rating.choices, default=Rating.One.value)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    file = models.FileField(upload_to='comments/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

class Image(models.Model):
    image = models.ImageField(upload_to='images/products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)
    def __str__(self):
        return self.product.name