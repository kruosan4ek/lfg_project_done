"""
Модели приложения LFG: игры, ранги, роли, объявления, кланы, отзывы.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    """
    Игра, для которой можно искать тиммейтов.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    logo = models.ImageField(upload_to='games/logos/', blank=True, verbose_name='Логотип')
    description = models.TextField(blank=True, verbose_name='Описание')
    max_team_size = models.PositiveIntegerField(default=5, verbose_name='Размер команды')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name


class Rank(models.Model):
    """
    Ранг/звание в игре.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ranks', verbose_name='Игра')
    name = models.CharField(max_length=50, verbose_name='Название')
    order = models.PositiveIntegerField(verbose_name='Порядок сортировки')

    class Meta:
        ordering = ['order']
        unique_together = ['game', 'name']
        verbose_name = 'Ранг'
        verbose_name_plural = 'Ранги'

    def __str__(self):
        return f"{self.name} ({self.game.name})"


class Role(models.Model):
    """
    Роль в игре (саппорт, керри, танк и т.д.).
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='roles', verbose_name='Игра')
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        unique_together = ['game', 'name']
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return f"{self.name} ({self.game.name})"


class LFGPost(models.Model):
    """
    Объявление о поиске группы (Looking For Group).
    """
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('closed', 'Закрыто'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lfg_posts',
        verbose_name='Автор'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='lfg_posts',
        verbose_name='Игра'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    required_rank = models.ForeignKey(
        Rank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Требуемый ранг'
    )
    required_roles = models.ManyToManyField(Role, blank=True, verbose_name='Требуемые роли')
    voice_chat_required = models.BooleanField(default=False, verbose_name='Голосовой чат обязателен')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Clan(models.Model):
    """
    Клан/гильдия.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    tag = models.CharField(max_length=10, unique=True, verbose_name='Тег')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='clans', verbose_name='Игра')
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='led_clans',
        verbose_name='Лидер'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ClanMembership',
        related_name='clans',
        verbose_name='Участники'
    )
    logo = models.ImageField(upload_to='clans/logos/', blank=True, verbose_name='Эмблема')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Клан'
        verbose_name_plural = 'Кланы'

    def __str__(self):
        return f"[{self.tag}] {self.name}"


class ClanMembership(models.Model):
    """
    Членство в клане (промежуточная модель).
    """
    ROLE_CHOICES = [
        ('leader', 'Лидер'),
        ('officer', 'Офицер'),
        ('member', 'Участник'),
    ]

    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, verbose_name='Клан')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member', verbose_name='Роль')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='Присоединился')

    class Meta:
        unique_together = ['clan', 'user']
        verbose_name = 'Членство в клане'
        verbose_name_plural = 'Членства в кланах'

    def __str__(self):
        return f"{self.user.username} в {self.clan.name}"


class Review(models.Model):
    """
    Отзыв о игроке после совместной игры.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        verbose_name='Автор отзыва'
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name='Цель отзыва'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    comment = models.TextField(verbose_name='Комментарий')
    is_toxic = models.BooleanField(default=False, verbose_name='Токсичный игрок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        unique_together = ['author', 'target']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.author} для {self.target}"