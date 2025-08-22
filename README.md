# Django-RealWorld (Conduit) — modernized RealWorld example

**Полный стек:** Backend — Django + DRF (Poetry, `pyproject.toml`), Frontend — React + Redux (Create React App).

Проект — модернизация Conduit (RealWorld). Включает: статьи, комментарии, теги, избранное, ленту, профили, кастомную аутентификацию (access/refresh tokens + refresh в cookie).

---

## Структура репозитория

```
/ (root)
├─ backend/               # Django проект
│  ├─ manage.py
│  ├─ pyproject.toml
│  ├─ poetry.lock
│  ├─ .env.example
│  ├─ articles/
│  ├─ comments/
│  ├─ profiles/
│  ├─ tags/
│  ├─ myauth/
│  └─ core/
├─ frontend/              # React + Redux (CRA)
│  ├─ package.json
│  ├─ public/
│  └─ src/
└─ api/                   # Postman collections
   ├─ Conduit.postman_collection.json
   └─ conduit_new.postman_collection.json
```

> В `backend/` есть `.env.example` — используйте его как шаблон для локальной конфигурации.

---

## Быстрый старт (локальная разработка)

### Требования

* Python 3.12+
* Poetry
* Node.js (LTS) + npm
* (Опционально) PostgreSQL — для продакшена; по умолчанию можно использовать SQLite

### Запуск (пример)

```bash
# Клонируем репозиторий
git clone https://github.com/<you>/<repo>.git
cd <repo>

# Backend
cd backend
poetry install
cp .env.example .env    # отредактируйте .env при необходимости
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver 0.0.0.0:8000

# В другом терминале — Frontend
cd ../frontend
npm install
npm start               # dev server, обычно http://localhost:4100
```

После старта frontend ожидает API по `http://localhost:8000/api`. При необходимости поправьте `frontend/src/agent.js` (переменная `API_ROOT`).

---

## Backend — подробности

### Управление зависимостями

Проект использует **Poetry** и `pyproject.toml`:

```bash
cd backend
poetry install
poetry shell   # опционально
```

### Переменные окружения

Скопируйте `backend/.env.example` в `backend/.env` и заполните значения. Пример минимального `.env` для разработки:

```
SECRET_KEY=dev-secret
DEBUG=True
DATABASE_URL=sqlite:///./db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:4100
CORS_ALLOW_CREDENTIALS=True
ACCESS_TOKEN_LIFETIME=5m
REFRESH_TOKEN_LIFETIME=7d
```

> Внимание: точные имена переменных зависят от реализации `settings.py` — проверьте `backend/conduit/settings.py`.

### Команды

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

## Frontend — подробности

### Установка и запуск

```bash
cd frontend
npm install
npm start
```

### Настройка API

Проверьте `frontend/src/agent.js` (переменная `API_ROOT`) и при необходимости поменяйте URL на `http://localhost:8000/api`.

### Особенности

* Реализован refresh токена: `agent` использует `withCredentials()` и endpoint `/api/token/refresh/`.
* В некоторых местах фронтенд tolerant к разным названиям полей (например `tags` vs `tagList`) — см. редьюсеры `home`/`articleList`.

---

## API / тестирование

В папке `/api/` находятся Postman коллекции для тестирования:

* `Conduit.postman_collection.json`
* `conduit_new.postman_collection.json`

Используйте их для проверки endpoints: авторизация, статьи, комментарии, теги, избранное, профиль.
