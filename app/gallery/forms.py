from django import forms

from .models import Image, Favorite


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'signature']


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        exclude = ['author', 'image']
