from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from gallery.models import Favorite
from gallery.serializer import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
