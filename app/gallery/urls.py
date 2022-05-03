from django.urls import path

from .views import ImageListView, ImageCreateView, ImageUpdateView, ImageDetailView, ImageDeleteView, FavoriteAddView

image_urls = [
    path('', ImageListView.as_view(), name='image_list'),
    path('image/create/', ImageCreateView.as_view(), name='image_create'),
    path('image/update/<int:pk>', ImageUpdateView.as_view(), name='image_update'),
    path('image/detail/<int:pk>', ImageDetailView.as_view(), name='image_detail'),
    path('image/delete/<int:pk>', ImageDeleteView.as_view(), name='image_delete'),
    ]

favorite_urls = [
    path('image/<int:pk>/favorite/add', FavoriteAddView.as_view(), name='favorite_add'),
]

urlpatterns = image_urls
urlpatterns += favorite_urls
