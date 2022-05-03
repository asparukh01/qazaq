from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='gallery_pics', null=False, blank=False, verbose_name='Image')
    signature = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE,
        verbose_name='Author', related_name='images', null=False, blank=False)
    favorite = models.IntegerField(
        default=0,
        blank=True,
        validators=(MinValueValidator(0),)
    )

    def __str__(self):
        return self.signature


class Favorite(models.Model):
    image = models.ForeignKey(
        to='gallery.Image', on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Favorite'
    )
    author = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE,
        verbose_name='Author', related_name='favorites'
    )

    class Meta:
        unique_together = ['author', 'image']
