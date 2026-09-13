# 🎮 LFG — Looking For Group

Платформа для поиска тиммейтов в онлайн-игры без токсиков.

## 🎯 Проблема
Долгий поиск адекватных сокомандников и высокая токсичность в соревновательных играх.

## 💡 Решение
LFG позволяет создавать объявления о поиске команды с фильтрацией по играм, рангам и ролям. Встроенная система отзывов и репутации помогает отсеивать неадекватных игроков.

## 👥 Целевая аудитория
Геймеры, играющие в командные онлайн-игры (CS2, Dota 2, Valorant, LoL).

## 🛠 Технологии
- **Backend:** Django 5.x, Django REST Framework
- **WebSockets:** Django Channels
- **БД:** PostgreSQL 16 (SQLite для разработки)
- **Аутентификация:** OAuth2 (GitHub, VK)
- **Документация API:** drf-spectacular (Swagger)
- **Контейнеризация:** Docker + docker-compose
- **CI/CD:** GitHub Actions

## 🚀 Быстрый старт через Docker

### Требования
- Docker Desktop
- Git

### Запуск

```bash
# 1. Клонируй репозиторий
git clone https://github.com/твой_username/lfg_project.git
cd lfg_project

# 2. Скопируй переменные окружения
cp .env.example .env

# 3. Запусти проект
docker-compose up --build

# 4. В новом терминале создай суперпользователя
docker-compose exec web python manage.py createsuperuser

# 5. Заполни БД тестовыми данными
docker-compose exec web python manage.py seed_db
```

Открой: **http://localhost:8000/**

### Тестовые пользователи (пароль: `testpass123`)
- `shadow`
- `dragon`
- `phoenix`
- `viper`

## 💻 Локальный запуск (без Docker)

```bash
# 1. Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Миграции
python manage.py migrate

# 4. Тестовые данные
python manage.py seed_db

# 5. Суперпользователь
python manage.py createsuperuser

# 6. Запуск
python manage.py runserver
```

## 📡 API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/posts/` | Список объявлений (фильтр: `?game=1&voice_chat=true`) |
| GET | `/api/posts/<id>/` | Детали объявления |
| GET | `/api/users/<username>/` | Профиль пользователя |
| GET | `/api/me/` | Текущий пользователь |
| GET | `/api/games/` | Список игр |
| GET | `/api/clans/` | Список кланов |

**Swagger UI:** http://localhost:8000/api/docs/

## 💬 WebSockets

Чат в объявлении: `ws://localhost:8000/ws/chat/<post_id>/`

## 🧪 Тесты

```bash
pytest
pytest --cov=lfg --cov=accounts
```

## 🎯 Функциональность

- ✅ Регистрация, вход, выход, сброс пароля
- ✅ OAuth2 (GitHub, VK)
- ✅ Создание/редактирование/удаление объявлений
- ✅ Фильтрация по играм, рангам, ролям
- ✅ Живой чат на WebSockets
- ✅ Кланы и членство
- ✅ Система отзывов и репутации
- ✅ Избранное через сессии
- ✅ REST API + Swagger
- ✅ Docker + CI/CD
- ✅ Покрытие тестами

## 📄 Лицензия
MIT
