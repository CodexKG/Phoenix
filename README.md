```markdown
# DaryLesa Project

Этот проект настроен для работы с Docker и включает конфигурации для локальной и продакшн среды.

## Структура проекта

```plaintext
Phoenix/
├── apps/
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker/
│   ├── docker-compose.local.yml
│   ├── docker-compose.server.yml
├── media/
├── nginx/
│   ├── nginx.conf
│   ├── nginx.server.conf
├── static/
├── templates/
├── venv/
├── .env
├── .env.example
├── .gitignore
├── db.json
├── Dockerfile
├── manage.py
├── requirements.txt
└── shellscripts/
    └── entrypoint.sh
```

## Установка и настройка

### Предварительные требования

- Docker
- Docker Compose

### Настройка окружения

1. Создайте файл `.env` в корне проекта и заполните его переменными окружения. Пример можно найти в `.env.example`.

### Сборка и запуск контейнеров

#### Локальная среда

1. Сборка и запуск контейнеров:
    ```sh
    docker-compose -f docker/docker-compose.local.yml up --build
    ```

2. Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).

#### Продакшн среда

1. Сборка и запуск контейнеров:
    ```sh
    docker-compose -f docker/docker-compose.server.yml up --build -d
    ```

2. Приложение будет доступно по адресу: [http://your_domain](http://your_domain) (замените `your_domain` на ваш реальный домен).

## Конфигурация Nginx

### Локальная среда

Файл конфигурации: `nginx/nginx.local.conf`

### Продакшн среда

Файл конфигурации: `nginx/nginx.server.conf`

Для настройки SSL сертификатов, разместите их в папке `certs` и укажите правильные пути в конфигурации Nginx.

## Скрипт начальной настройки

Скрипт `entrypoint.sh` выполняет автоматические миграции при запуске контейнеров. Он находится в папке `shellscripts`.

## Загрузка данных из db.json

Чтобы загрузить данные из `db.json` в вашу базу данных, выполните следующую команду после запуска контейнеров:

```sh
docker-compose exec web python manage.py loaddata db_new.json
```

Эта команда выполнит загрузку данных из файла `db.json` в вашу базу данных.

## Полезные команды

- Остановка контейнеров:
    ```sh
    docker-compose -f docker/docker-compose.local.yml down
    ```

- Остановка контейнеров продакшн среды:
    ```sh
    docker-compose -f docker/docker-compose.server.yml down
    ```

- Просмотр логов:
    ```sh
    docker-compose -f docker/docker-compose.local.yml logs -f
    ```

- Просмотр логов продакшн среды:
    ```sh
    docker-compose -f docker/docker-compose.server.yml logs -f
    ```
