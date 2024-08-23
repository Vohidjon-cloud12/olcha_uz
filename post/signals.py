from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from post.models import Post


@receiver(post_save, sender=Post)
@receiver(pre_save, sender=Post)
def Clear_cache(sender, instance, **kwargs):
    cache.delete('post_list')
    print('Post List cache cleared')
    post_id=instance.id
    cache.delete(f'post_list/{post_id}')
    print('Post Deatil cache cleared')