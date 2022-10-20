# Сервис авторизации

## Как запустить
- Скопируйте .env файлы: 

    - .env для API - `cp ./app/.env.example ./app/.env`
    
    - .env для Docker сборки - `cp ./.env.example ./.env`
    
- `docker-compose up -d`

## Подготовительные работы
- Накатить миграции:

    `docker-compose exec auth-app flask db upgrade`

- Создать админа:

    `docker-compose exec auth-app flask create-super-user adminlogin adminpass`

- Запустить тесты (на текущей БД):

    `docker-compose exec auth-app pytest`

## Сервисы
- API: http://localhost:8100/apidocs