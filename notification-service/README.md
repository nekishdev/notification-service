# Сервис нотификаций

## Как запустить
- Скопируйте .env файлы: 

    - .env для API - `cp ./api/.env.example ./api/.env`
    
    - .env для Docker сборки - `cp ./.env.example ./.env`
    
- `docker-compose up -d`

## Подготовительные работы
- Запустить тесты:

    `docker-compose exec notification-api pytest`

## Сервисы
- API: http://localhost:8400/docs
- RabbitMQ web panel: http://localhost:8402 (логин - guest, пароль - guest)