# YourOwnGame Backend (FastAPI)

Локальный backend для викторины в стиле «Своя игра». Вся игровая логика хранится на сервере: шаблоны, сессии, состояния вопросов, очки команд и определение победителя.

## Стек
- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy ORM
- Pydantic
- Alembic
- SQLite
- python-dotenv / pydantic-settings

## Структура
```
backend/
  app/
    api/routes/
    core/
    crud/
    db/
    models/
    schemas/
    services/
    seed.py
    main.py
  alembic/
    versions/
  alembic.ini
  requirements.txt
  .env.example
```

## Установка и запуск
1. Перейдите в backend:
   ```bash
   cd backend
   ```
2. Создайте venv и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Создайте `.env`:
   ```bash
   cp .env.example .env
   ```
4. Примените миграции:
   ```bash
   alembic upgrade head
   ```
5. Заполните демо-данные:
   ```bash
   python -m app.seed
   ```
6. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

Swagger UI: http://localhost:8000/docs

## Подключение React frontend
На фронтенде используйте базовый URL `http://localhost:8000/api`.
Убедитесь, что frontend работает с `localhost:5173` или `localhost:3000` (CORS уже настроен).

## Примеры API-запросов
### Проверка здоровья
```bash
curl http://localhost:8000/api/health
```

### Получить шаблоны
```bash
curl http://localhost:8000/api/templates
```

### Создать сессию
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": 1,
    "teams": [
      {"name":"Команда А","display_order":0},
      {"name":"Команда Б","display_order":1}
    ]
  }'
```

### Начать игру
```bash
curl -X POST http://localhost:8000/api/sessions/1/start
```

### Открыть вопрос
```bash
curl -X POST http://localhost:8000/api/sessions/1/questions/1/open \
  -H "Content-Type: application/json" \
  -d '{"selected_by_team_id":1}'
```

### Показать ответ и закрыть вопрос
```bash
curl -X POST http://localhost:8000/api/sessions/1/questions/1/reveal-answer
curl -X POST http://localhost:8000/api/sessions/1/questions/1/close
```

### Изменить счёт команды
```bash
curl -X PATCH http://localhost:8000/api/sessions/1/teams/1/score \
  -H "Content-Type: application/json" \
  -d '{"delta":100}'
```
