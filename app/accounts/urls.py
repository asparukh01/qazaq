from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ProfileView,

    ProfileUpdateView,
    ChangePasswordView,
)

accounts_urls = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('change_password', ChangePasswordView.as_view(), name='change_password')
]

urlpatterns = accounts_urls