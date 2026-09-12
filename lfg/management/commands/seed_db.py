"""
Management-команда для заполнения БД тестовыми данными.
Запуск: python manage.py seed_db
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lfg.models import Game, Rank, Role, LFGPost, Clan, ClanMembership, Review

User = get_user_model()


class Command(BaseCommand):
    """Заполняет базу данных тестовыми данными."""

    help = 'Создаёт тестовые данные: игры, ранги, роли, пользователей, объявления'

    def handle(self, *args, **kwargs):
        """Основная логика команды."""
        self.stdout.write(self.style.WARNING('Начинаем заполнение БД...'))

        # 1. Игры
        games_data = [
            {'name': 'Counter-Strike 2', 'slug': 'cs2', 'max_team_size': 5,
             'description': 'Тактический шутер 5v5'},
            {'name': 'Dota 2', 'slug': 'dota2', 'max_team_size': 5,
             'description': 'MOBA 5v5'},
            {'name': 'Valorant', 'slug': 'valorant', 'max_team_size': 5,
             'description': 'Тактический шутер с агентами'},
            {'name': 'League of Legends', 'slug': 'lol', 'max_team_size': 5,
             'description': 'MOBA 5v5'},
        ]

        games = {}
        for g in games_data:
            game, _ = Game.objects.get_or_create(slug=g['slug'], defaults=g)
            games[g['slug']] = game
            self.stdout.write(f'  + Игра: {game.name}')

        # 2. Ранги для CS2
        cs2 = games['cs2']
        ranks_cs2 = ['Silver', 'Gold Nova', 'Master Guardian',
                     'Legendary Eagle', 'Global Elite']
        for i, rank_name in enumerate(ranks_cs2):
            Rank.objects.get_or_create(
                game=cs2, name=rank_name,
                defaults={'order': i + 1},
            )
        self.stdout.write(f'  + Ранги для {cs2.name}: {len(ranks_cs2)}')

        # 3. Роли для всех игр
        roles_data = {
            'cs2': ['Rifler', 'AWPer', 'IGL', 'Support', 'Entry'],
            'dota2': ['Carry', 'Mid', 'Offlane', 'Soft Support', 'Hard Support'],
            'valorant': ['Duelist', 'Controller', 'Initiator', 'Sentinel'],
            'lol': ['Top', 'Jungle', 'Mid', 'ADC', 'Support'],
        }
        for slug, roles in roles_data.items():
            for role_name in roles:
                Role.objects.get_or_create(game=games[slug], name=role_name)
            self.stdout.write(f'  + Роли для {games[slug].name}: {len(roles)}')

        # 4. Пользователи
        users_data = [
            {'username': 'shadow', 'email': 'shadow@lfg.com'},
            {'username': 'dragon', 'email': 'dragon@lfg.com'},
            {'username': 'phoenix', 'email': 'phoenix@lfg.com'},
            {'username': 'viper', 'email': 'viper@lfg.com'},
        ]
        users = []
        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={'email': u['email']},
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
            self.stdout.write(f'  + Пользователь: {user.username}')

        # 5. LFG объявления
        posts_data = [
            {'title': 'Ищу команду для катки', 'game': cs2, 'author': users[0],
             'description': 'Голд Нова, ищу адекватных ребят для ранкеда',
             'voice_chat_required': True},
            {'title': 'Нужен саппорт для турнира', 'game': games['dota2'],
             'author': users[1],
             'description': 'Играем в турнире, нужен опытный саппорт',
             'voice_chat_required': True},
            {'title': 'Казуальная катка вечером', 'game': games['valorant'],
             'author': users[2],
             'description': 'Просто поиграть без напряга, без рейтинга',
             'voice_chat_required': False},
            {'title': 'Собираем стак на вечер', 'game': games['lol'],
             'author': users[3],
             'description': 'Голд-платина, ищем ADC и мид',
             'voice_chat_required': True},
        ]

        for p in posts_data:
            post, created = LFGPost.objects.get_or_create(
                title=p['title'],
                defaults=p,
            )
            if created:
                self.stdout.write(f'  + Объявление: {post.title}')

        # 6. Клан
        clan, created = Clan.objects.get_or_create(
            name='Phoenix Squad',
            defaults={
                'tag': 'PHX',
                'game': cs2,
                'leader': users[0],
                'description': 'Топовый клан для серьёзных игроков',
            },
        )
        if created:
            ClanMembership.objects.create(clan=clan, user=users[0], role='leader')
            ClanMembership.objects.create(clan=clan, user=users[1], role='member')
            self.stdout.write(f'  + Клан: {clan.name}')

        # 7. Отзывы
        Review.objects.get_or_create(
            author=users[0], target=users[1],
            defaults={'rating': 5, 'comment': 'Отличный тиммейт, всегда на связи!'},
        )
        Review.objects.get_or_create(
            author=users[1], target=users[0],
            defaults={'rating': 4, 'comment': 'Хороший игрок, но иногда тильтует'},
        )
        self.stdout.write('  + Отзывы созданы')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
        self.stdout.write(self.style.WARNING(
            '\nТестовые пользователи (пароль: testpass123):\n'
            '  - shadow\n  - dragon\n  - phoenix\n  - viper'
        ))