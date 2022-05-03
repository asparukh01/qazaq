from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    image = models.ImageField(null=True, blank=True, upload_to='uploads/user_pics', verbose_name='Аватар')
    about = models.TextField(max_length=3000, null=True)

    def __str__(self):
        return self.user.get_full_name() + "' s profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

        permissions = [
            ('list_view', 'View users')
        ]