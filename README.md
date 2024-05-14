# Интернет-магазин MEGANO
Владелец торгового центра во время COVID-карантина решил перевести своих арендодателей в онлайн. Сделать это он намерен с помощью создания платформы, на которой продавцы смогут разместить информацию о себе и своём товаре. Онлайновый торговый центр или, другими словами, интернет-магазин, являющийся агрегатором товаров различных продавцов.

## Как установить
Для работы сервиса требуются:
- Python версии не ниже 3.10.
- установленное ПО для контейнеризации - [Docker](https://docs.docker.com/engine/install/).
- Инструмент [poetry](https://python-poetry.org/) для управления зависимостями и сборкой пакетов в Python.

Настройка переменных окружения
1. Скопируйте файл .env.dist в .env
2. Заполните .env файл. Пример:
```yaml
DATABASE_URL = postgresql://skillbox:secret@127.0.0.1:5436/market
REDIS_URL = redis://127.0.0.1:6379/0
```

Запуск СУБД Postgresql
```shell
docker run --name skillbox-db-36 -e POSTGRES_USER=skillbox -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=market -p 5436:5432 -d postgres
```
Запуск брокера сообщений REDIS
```shell
docker run --name redis-db -d -p 6379:6379 redis
```
Установка и активация виртуального окружения
```shell
poetry install  ; установка пакетов
poetry shell  ; активация виртуального окружения
pre-commit install  ; установка pre-commit для проверки форматирования кода, см. .pre-commit-config.yaml
```
### Как удалить контейнеры
СУБД Postgres
```shell
docker rm -f -v skillbox-db-36
```

Брокер сообщений REDIS
```shell
docker rm -f -v redis-db
```

## Проверка форматирования кода
Проверка кода выполняется из корневой папки репозитория.
* Анализатор кода flake8
```shell
flake8 market
```

* Линтер black
```shell
black market
```

## Как запустить web-сервер
Запуск сервера производится в активированном локальном окружение из папки `market/`
```shell
python manage.py runserver 0.0.0.0:8000
```

## Как создать файлы .po для перевода
Запуск команды производится в активированном локальном окружении из папки `market/`
Это команда для того, чтобы в файле .ро создались сторки для перевода из вайлов с разрешением .jinja2
```shell
python manage.py makemessages -l en --extension jinja2 --extension py
```


## Как запустить настройки i18n
Запуск i18n производится в активированном локальном окружении из папки `market/`
```shell
python manage.py compilemessages
```

## Запуск Celery
Запуск производится в активированном локальном окружении из папки `market/`
Celery-Worker:
```shell
celery -A market.config worker -l info
```
Celery-Beat:
```shell
celery -A market.config beat -l info
```


## Логин и пароль для суперпользователя
login: demon_at@mail.ru
password: 61903991shalaikodima
## Логин и пароль для покупателя
login: buyer@example.com
password: 61903991shalaikodima
## Логин и пароль для продавца
login: salesman@example.com
password: 61903991shalaikodima
