
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from app.models import Product


@receiver(pre_save, sender=Product)
@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def delete_saved_product(sender, instance, **kwargs):
    category_slug = kwargs.get('slug')
    group_slug = kwargs.get('slug')
    cache.delete(f'product_list_{category_slug}_{group_slug}')
    cache.delete(f'product_detail_{instance.id}')


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Product

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    # Product list keshini tozalash
    category_slug = instance.group.category.slug if instance.group and instance.group.category else None
    group_slug = instance.group.slug if instance.group else None

    # Kesh kalitlarini yaratish
    list_cache_key = f'product_list_{category_slug}_{group_slug}'
    detail_cache_key = f'product_detail_{instance.slug}'

    # Keshni tozalash
    cache.delete(list_cache_key)
    cache.delete(detail_cache_key)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     if created:
#         Token.objects.create(user=instance)



