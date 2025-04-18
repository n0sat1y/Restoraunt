# Сервис бронирования столиков в ресторане

## Как запустить:
	1. Установите Docker и Docker Compose
	2. В корне проекта выполните:
	docker-compose up -d --build
	3. Сервис будет доступен по адресу http://localhost:8000

## Основные возможности:
	- Просмотр всех столиков (GET /tables/)
	- Добавление нового столика (POST /tables/)
	- Удаление столика (DELETE /tables/{id})
	- Просмотр всех броней (GET /reservations/)
	- Создание новой брони (POST /reservations/)
	- Удаление брони (DELETE /reservations/{id})

## Особенности:
	- Проверка на пересечение времени бронирования
	- Логирование всех операций
	- Базовые тесты

## Используемые технологии:
FastAPI, PostgreSQL, SQLAlchemy, Docker

## Документация API доступна после запуска:
	- http://localhost:8000/docs (Swagger)
	- http://localhost:8000/redoc (ReDoc)