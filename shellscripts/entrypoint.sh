#!/bin/sh

# Запускаем RabbitMQ сервер в фоне
rabbitmq-server -detached

# Подождите, пока база данных будет доступна
until nc -z -v -w30 db_phoenix 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

# Подождите, пока RabbitMQ будет доступен на порту 12000
until nc -z -v -w30 localhost 12000
do
  echo "Waiting for RabbitMQ connection on port 12000..."
  sleep 5
done

# Выполните миграции
python manage.py migrate

# Соберите статические файлы
python manage.py collectstatic --noinput

# Запустите команду (gunicorn)
exec "$@"