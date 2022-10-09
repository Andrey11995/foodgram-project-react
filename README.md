# Проект Foodgram «Продуктовый помощник»
![push](https://github.com/Andrey11995/foodgram-project-react/actions/workflows/workflow.yml/badge.svg?event=push)
## Описание:

#### Проект Foodgram представляет собой одностраничное приложение на фреймворке React и API для него на Django REST Framework. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

![Image](https://github.com/Andrey11995/foodgram-project-react/raw/master/backend/static/foodgram.jpg)

## Наполнение env-файла:

- SECRET_KEY - секретный ключ Django;
- DEBUG - 1 - вкл, 0 - выкл;
- ALLOWED_HOSTS - список доступных хостов через запятую без пробела (localhost,127.0.0.1);
- POSTGRES_USER - логин для подключения к БД;
- POSTGRES_PASSWORD - пароль для подключения к БД;
- POSTGRES_DB - название базы данных;
- DB_HOST - название сервиса (контейнера);
- DB_PORT - порт для подключения к БД;


## Как запустить проект в контейнерах:

Клонировать репозиторий и перейти в директорию с файлом docker-compose.yaml:

```
git clone https://github.com/Andrey11995/foodgram-project-react
```

```
cd foodgram-project-react/infra/
```

Создать файл .env и наполнить его данными:

```
touch .env && nano .env
```

Запустить Docker-compose:

```
docker-compose up -d --build
```
Проект развернут и запущен, миграции, сборка статики и наполнение БД ингредиентами автоматизированы


### Создание суперпользователя:

```
docker-compose exec backend python manage.py createsuperuser
```
Ввести почту, логин, имя, фамилию и пароль.

>❗️Внимание❗️ Команда выполняется только из директории, содержащей файл docker-compose.yml

## Технологии

- Python 3.7
- Django REST Framework
- React
- PostgreSQL, SQLite
- Docker
- Nginx
- Gunicorn
- Github Workflow
