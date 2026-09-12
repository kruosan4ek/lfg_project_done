"""
Тесты для приложения LFG.
Проверяет модели Game, LFGPost и API эндпоинт /api/posts/.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from lfg.models import Game, LFGPost

User = get_user_model()


class GameModelTest(TestCase):
    """Тесты модели Game."""

    def setUp(self):
        """Создаёт тестовую игру перед каждым тестом."""
        self.game = Game.objects.create(
            name='Test Game',
            slug='test-game',
            max_team_size=5,
        )

    def test_game_creation(self):
        """Проверяет, что игра создаётся с правильными полями."""
        self.assertEqual(self.game.name, 'Test Game')
        self.assertEqual(self.game.slug, 'test-game')
        self.assertTrue(self.game.is_active)

    def test_game_str(self):
        """Проверяет строковое представление игры."""
        self.assertEqual(str(self.game), 'Test Game')


class LFGPostModelTest(TestCase):
    """Тесты модели LFGPost."""

    def setUp(self):
        """Создаёт пользователя, игру и объявление."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        self.game = Game.objects.create(name='CS2', slug='cs2')
        self.post = LFGPost.objects.create(
            author=self.user,
            game=self.game,
            title='Ищу команду',
            description='Голд Нова, ищу тиммейтов',
        )

    def test_post_creation(self):
        """Проверяет создание объявления."""
        self.assertEqual(self.post.title, 'Ищу команду')
        self.assertEqual(self.post.status, 'open')
        self.assertEqual(self.post.author, self.user)

    def test_post_default_status(self):
        """Проверяет, что новый пост открыт по умолчанию."""
        self.assertEqual(self.post.status, 'open')

    def test_post_str(self):
        """Проверяет строковое представление."""
        self.assertEqual(str(self.post), 'Ищу команду')


class LFGPostAPITest(TestCase):
    """Тесты API эндпоинта /api/posts/."""

    def setUp(self):
        """Создаёт данные и API-клиент."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123',
        )
        self.game = Game.objects.create(name='Dota 2', slug='dota2')
        self.post = LFGPost.objects.create(
            author=self.user,
            game=self.game,
            title='API Post',
            description='Testing API',
        )

    def test_list_posts(self):
        """Проверяет, что API возвращает список постов."""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_game(self):
        """Проверяет фильтрацию постов по ID игры."""
        response = self.client.get(f'/api/posts/?game={self.game.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_filter_empty_result(self):
        """Проверяет, что фильтр по чужой игре возвращает 0."""
        other_game = Game.objects.create(name='Other', slug='other')
        response = self.client.get(f'/api/posts/?game={other_game.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)