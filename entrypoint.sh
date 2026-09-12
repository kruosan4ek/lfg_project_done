#!/bin/bash
set -e

echo "Ожидаем PostgreSQL..."
while ! pg_isready -h ${DB_HOST:-db} -p ${DB_PORT:-5432} -U ${DB_USER:-lfg_user}; do
    sleep 1
done

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Запускаем сервер..."
exec "$@"