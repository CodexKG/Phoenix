#!/bin/sh

# Запускаем RabbitMQ сервер в фоне
rabbitmq-server -detached

# Подождите, пока база данных будет доступна
until nc -z -v -w30 db_phoenix 5432
do
  echo "Waiting for database connection..."
  sleep 1
done

# Подождите, пока RabbitMQ будет доступен
until nc -z -v -w30 localhost 5672
do
  echo "Waiting for RabbitMQ connection..."
  sleep 1
done

# Выполните миграции
python manage.py migrate

# Соберите статические файлы
python manage.py collectstatic --noinput

# Запустите команду (gunicorn)
exec "$@"