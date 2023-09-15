[![Code checks](https://github.com/intomixins/SibDevApiStructure/actions/workflows/checks.yml/badge.svg)](https://github.com/intomixins/SibDevApiStructure/actions/workflows/checks.yml)

# Всего 4 запроса в базу данных для GET-запроса(включая 2 встроенных)!

# Cтек:
    Python3
    Django4
    DjangoRESTFramework
    Redis
    PostgeSQL
    Docker

# Описание:
Данный REST API позволяет получить топ 5 пользователей, потративших больше всего денег. Данные импортируются с помощью GET запроса. Все данные кэшируются.

Каждый клиент описывается следующими полями:
* username
* spent_money
* count_gems

# Запуск проекта с помощью Docker
*Клонировать репозиторий и перейти в рабочую директорию в командной строке:*
```
https://github.com/intomixins/SibDevApiStructure/
```
```
cd SibDevApiStructure/
```
*Делаем сборку и поднимаем контейнер:*
```
docker-compose build
docker-compose up
```
*В дополнительном окне терминала выполняем миграции:*
```
docker-compose exec web python manage.py migrate
```

API доступно по следующему URL:
http://127.0.0.1:8000/api/v1/
