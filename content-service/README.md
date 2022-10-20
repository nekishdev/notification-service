# Сервис контента

## Как запустить
- Скопируйте .env файлы 

    `cp ./admin/config/.env.example ./admin/config/.env`
    
    `cp ./etl/.env.example ./etl/.env`
    
    `cp ./api/.env.example ./api/.env`
    
    `cp ./.env.example ./.env`
    
- `docker-compose up -d`

- Создать супер-пользователя для админки: `docker-compose exec film-admin python manage.py createsuperuser`

## Сервисы
- Admin panel: http://localhost:8200/admin

- API: http://localhost:8202/api/openapi
