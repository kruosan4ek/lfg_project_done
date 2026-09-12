"""
Модели приложения accounts.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями для геймера.
    """
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    discord_tag = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Discord'
    )
    steam_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Steam ID'
    )
    reputation_score = models.FloatField(
        default=0.0,
        verbose_name='Рейтинг репутации'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username