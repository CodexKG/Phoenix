#!/bin/sh

# Запускаем RabbitMQ сервер в фоне
rabbitmq-server -detached

# Подождите, пока база данных будет доступна
until nc -z -v -w30 db_phoenix 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

# Подождите, пока RabbitMQ будет доступен на порту 5672
until nc -z -v -w30 rabbitmq_phoenix 5672
do
  echo "Waiting for RabbitMQ connection on port 5672..."
  sleep 5
done

# python manage.py makemigrations

# Выполните миграции
python manage.py migrate

# Соберите статические файлы
python manage.py collectstatic --noinput

# Запустите команду (gunicorn)
exec "$@"