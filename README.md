# Проект онлайн-кинотеатра

## Сервисы
- [Сервис авторизации](auth-service/README.md)
- [Сервис контента](content-service/README.md)
- [Сервис UGC](ugc-service/README.md)
- [Сервис логирования](logging-service/README.md)
- [Сервис нотификаций](notification-service/README.md)

### Действия перед запуском
- Создать общую сеть чтобы сервисы могли достучаться друг до друга: `docker network create backend-external` (сеть `backend-external` уже прописана в env всех сервисов)