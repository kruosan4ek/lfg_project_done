"""
Сериализаторы для API.
"""
from rest_framework import serializers
from lfg.models import LFGPost, Game
from accounts.models import User


class GameSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Game."""
    class Meta:
        model = Game
        fields = ['id', 'name', 'slug', 'description', 'max_team_size']


class LFGPostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели LFGPost."""
    author_username = serializers.CharField(source='author.username', read_only=True)
    game_name = serializers.CharField(source='game.name', read_only=True)

    class Meta:
        model = LFGPost
        fields = [
            'id', 'title', 'description', 'author_username', 'game_name',
            'voice_chat_required', 'status', 'created_at'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta:
        model = User
        fields = ['id', 'username', 'discord_tag', 'steam_id', 'reputation_score', 'bio', 'avatar']