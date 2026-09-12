"""
URL маршруты для приложения LFG.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('lfg/create/', views.lfg_create_view, name='lfg_create'),
    path('lfg/<int:pk>/', views.lfg_detail_view, name='lfg_detail'),
    path('lfg/<int:pk>/edit/', views.lfg_update_view, name='lfg_update'),
    path('lfg/<int:pk>/delete/', views.lfg_delete_view, name='lfg_delete'),
    path('lfg/<int:pk>/chat/', views.chat_room_view, name='chat_room'),   # ← ЭТА СТРОКА
    path('clans/', views.clan_list_view, name='clan_list'),
    path('clans/create/', views.clan_create_view, name='clan_create'),
    path('clans/<int:pk>/', views.clan_detail_view, name='clan_detail'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<int:post_id>/', views.add_to_favorites, name='add_to_favorites'),
]