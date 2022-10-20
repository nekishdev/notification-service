# Сервис UGC

## Как запустить

- Скопируйте .env файлы     

    Основной .env для сборки - `cp ./.env.example ./.env`

    .env для API - `cp ./api/.env.example ./api/.env`
    
    .env для ETL - `cp ./api/.env.example ./api/.env`

- Для запуска контейнеров в корне проекта выполняем:

    `docker-compose up -d`

## Взаимодействие

- API: http://localhost:8300/apidocs (./.env - API_LOCAL_PORT).

- Kibana: Просмотр логов http://localhost:8314 (./.env - KIBANA_LOCAL_PORT)


## Логи

Для отображения логов в Kibana требуется завести Index Pattern

Чтобы завести паттерн, перейдите в Management → Stack Management → Index Patterns и нажмите Create index pattern.

После создания паттерна перейдите в Kibana → Discover, чтобы посмотреть содержимое индексов.