from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Favorite, Image


@receiver(signal=post_save, sender=Favorite)
def add_like_post(sender, instance, created, **kwargs):
    if created:
        post = Image.objects.get(pk=instance.image.id)
        post.favorite += 1
        post.save()
