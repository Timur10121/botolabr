# BOTOLABR — Конструктор Telegram-ботов

SPA на Vue 3 + FastAPI + SQLite. Визуальный редактор сценариев, webhook, управление ботами.

---

## Быстрый запуск

### Backend

```bash
cd botolabr_new\backend 
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (dev)

```bash
cd botolabr_new\frontend
npm install
npm run dev
```

Открыть: http://localhost:5173

cd botolabr_new\backend 
py polling.py

### Frontend (production build)

```bash
cd frontend
npm run build
# dist/ — готовая статика, раздавать через nginx или uvicorn StaticFiles
```

---

## Деплой для ВКР (ngrok)

1. Запустить backend: `uvicorn main:app --host 0.0.0.0 --port 8000`
2. Пробросить туннель: `ngrok http 8000`
3. В настройках бота указать URL ngrok как base_url для webhook

---

## Структура проекта

```
project/
├── backend/
│   ├── main.py             # FastAPI приложение, все роуты
│   ├── database.py         # SQLite, init_db, user_states хелперы
│   ├── models.py           # Pydantic модели
│   ├── scenario_engine.py  # Движок сценариев
│   ├── botolabr.db         # База данных (создаётся автоматически)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── main.js
    │   ├── App.vue
    │   ├── router/index.js
    │   ├── stores/auth.js
    │   ├── api/client.js
    │   ├── api/index.js
    │   ├── composables/useToast.js
    │   ├── components/
    │   │   ├── AppLayout.vue
    │   │   └── editor/
    │   │       ├── NodeCard.vue
    │   │       ├── Toolbar.vue
    │   │       └── ScenarioCanvas.vue
    │   └── views/
    │       ├── LoginView.vue
    │       ├── DashboardView.vue
    │       ├── BotsView.vue
    │       └── ScenarioEditorView.vue
    ├── package.json
    └── vite.config.js
```

---

## Типы блоков в редакторе

| Тип       | Описание                        |
|-----------|---------------------------------|
| message   | Отправка текстового сообщения   |
| buttons   | Inline-кнопки с переходами      |
| image     | Отправка изображения по URL     |
| delay     | Задержка (1–10 сек)             |
| input     | Ожидание ввода от пользователя  |
| condition | Ветвление по значению переменной|
| goto      | Переход к произвольному блоку   |
| end       | Завершение сценария             |

---

## API endpoints

| Метод  | URL                              | Описание                    |
|--------|----------------------------------|-----------------------------|
| POST   | /api/auth/register               | Регистрация                 |
| POST   | /api/auth/login                  | Вход                        |
| POST   | /api/auth/logout                 | Выход                       |
| GET    | /api/me                          | Текущий пользователь        |
| GET    | /api/bots                        | Список ботов                |
| POST   | /api/bots/check                  | Проверить токен Telegram    |
| POST   | /api/bots                        | Подключить бота             |
| DELETE | /api/bots/{id}                   | Удалить бота                |
| POST   | /api/bots/{id}/set-webhook       | Установить webhook          |
| DELETE | /api/bots/{id}/set-webhook       | Снять webhook               |
| GET    | /api/scenarios                   | Список сценариев            |
| POST   | /api/scenarios                   | Создать сценарий            |
| PATCH  | /api/scenarios/{id}              | Обновить сценарий           |
| DELETE | /api/scenarios/{id}              | Удалить сценарий            |
| POST   | /webhook/{bot_token}             | Telegram webhook            |
