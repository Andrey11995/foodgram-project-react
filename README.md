# Проект Foodgram «Продуктовый помощник»
![push](https://github.com/Andrey11995/foodgram-project-react/actions/workflows/workflow.yml/badge.svg?event=push)
## Описание:

### Проект Foodgram представляет собой одностраничное приложение на фреймворке React и API для него на Django REST Framework. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

![Image](https://github.com/Andrey11995/foodgram-project-react/raw/master/backend/static/foodgram.jpg)

## Наполнение env-файла:

- DB_ENGINE=django.db.backends.postgresql - используемая БД
- DB_NAME=postgres - имя БД
- POSTGRES_USER - логин для подключения к БД
- POSTGRES_PASSWORD - пароль для подключения к БД
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД


## Как запустить проект в контейнерах:

Клонировать репозиторий и перейти в директорию с файлом docker-compose.yaml:

```
git clone https://github.com/Andrey11995/foodgram-project-react
```

```
cd foodgram-project-react/infra/
```

Собрать проект в контейнеры и запустить:

```
docker-compose up -d --build
```

Выполнить миграции:

```
docker-compose exec backend python manage.py migrate
```

Собрать статические файлы:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

Создать суперпользователя:

```
docker-compose exec backend python manage.py createsuperuser
```
Потребуется ввести почту, имя пользователя и пароль.


## Наполнение базы данных

### Для наполнения базы данных ингредиентами необходимо применить следующую команду:

```
docker-compose exec backend python manage.py load_ingredients
```

## Автор

### Разработчик бэкенда - Андрей Завьялов


## Технологии

#### Python
#### Django REST Framework
#### React
#### PostgreSQL, SQLite
#### Gunicorn, Nginx
#### Docker, Docker-compose
#### CI и CD
