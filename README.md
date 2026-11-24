# SB1 — Доска объявлений (REST API)

Backend-часть веб-приложения «Доска объявлений» на Django и Django REST Framework.

## Стек технологий
- Python 3.12, Django 5.1, Django REST Framework
- PostgreSQL (основная БД), SQLite (тестовая БД)
- SimpleJWT + Djoser (JWT-аутентификация и сброс пароля по email)
- django-filter (поиск по названию объявления)
- drf-spectacular (документация OpenAPI / Swagger)
- Docker, Docker Compose, Nginx, Gunicorn
- GitHub Actions (CI/CD: pytest, flake8, Docker build, auto-deploy)

## Основные эндпоинты
- `POST /users/` — регистрация пользователя
- `GET /users/me/` — профиль текущего пользователя
- `POST /users/reset_password/` — запрос сброса пароля по email
- `POST /users/reset_password_confirm/` — подтверждение нового пароля
- `POST /token/` / `POST /token/refresh/` — получение и обновление JWT
- `GET /ads/` — список объявлений (пагинация по 4 объекта, поиск `?title=...`)
- `POST /ads/` — создание объявления
- `GET /ads/me/` — объявления текущего пользователя
- `GET /ads/{id}/`, `PATCH /ads/{id}/`, `DELETE /ads/{id}/` — детальный просмотр, редактирование и удаление
- `GET /ads/{ad_id}/comments/`, `POST /ads/{ad_id}/comments/` — отзывы к объявлению
- `GET /api/docs/` — интерактивная документация Swagger UI

## Локальный запуск
1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Скопируйте `.env.example` в `.env` и заполните переменные окружения.
3. Примените миграции и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Запуск через Docker Compose
```bash
docker compose up -d --build
```
Приложение будет доступно по адресу `http://localhost:8083/api/docs/`.

## Выполен деплой на удаленный сервер на ВМ Яндекс Cloud
Приложение доступно по адресу `http://158.160.132.249:8083/api/docs/`.


## Тестирование и проверка качества кода
```bash
pytest --cov=. --cov-report=term-missing
flake8 .
```