# Generated by Django 4.0.3 on 2022-04-09 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
