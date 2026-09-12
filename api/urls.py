"""
URL маршруты для API.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.LFGPostListAPIView.as_view(), name='api_posts'),
    path('users/<str:username>/', views.UserProfileAPIView.as_view(), name='api_user_profile'),
    path('games/', views.GameListAPIView.as_view(), name='api_games'),
]