"""
API представления.
"""
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from lfg.models import LFGPost, Game
from accounts.models import User
from .serializers import LFGPostSerializer, UserProfileSerializer, GameSerializer


class LFGPostListAPIView(generics.ListAPIView):
    """
    API для получения списка LFG объявлений с фильтрацией.
    """
    serializer_class = LFGPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = LFGPost.objects.filter(status='open')
        game_id = self.request.query_params.get('game')
        voice_chat = self.request.query_params.get('voice_chat')

        if game_id:
            queryset = queryset.filter(game_id=game_id)
        if voice_chat is not None:
            queryset = queryset.filter(voice_chat_required=voice_chat.lower() == 'true')

        return queryset.select_related('author', 'game')


class UserProfileAPIView(generics.RetrieveAPIView):
    """
    API для получения информации о пользователе.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'


class GameListAPIView(generics.ListAPIView):
    """
    API для получения списка игр.
    """
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer