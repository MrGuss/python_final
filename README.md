# Chat Application

Проект состоит из двух Python-сервисов и инфраструктуры для асинхронной обработки сообщений:

- `auth_service` - FastAPI-сервис регистрации, авторизации и выдачи JWT-токенов.
- `bot_service` - Telegram-бот, который проверяет JWT пользователя и отправляет запросы к LLM через OpenRouter.
- `RabbitMQ` - брокер задач Celery.
- `Redis` - хранилище JWT-токенов Telegram-пользователей и backend результатов Celery.
- `SQLite` - база данных пользователей Auth Service.

## Архитектура

Пользователь регистрируется или входит в систему через Auth Service и получает JWT. Затем он отправляет этот токен Telegram-боту командой `/token <jwt>`. Бот валидирует токен, сохраняет его в Redis на время жизни JWT и принимает текстовые сообщения пользователя.

Обработка LLM-запроса вынесена в Celery worker: бот кладет задачу в RabbitMQ, worker обращается к OpenRouter и отправляет ответ обратно в Telegram.

## Требования

- Docker и Docker Compose.
- Telegram Bot Token, полученный через BotFather.
- OpenRouter API Key.
- Python 3.11 и `uv` нужны только для локального запуска тестов без Docker.

## Переменные окружения

Перед запуском должны существовать файлы `auth_service/.env` и `bot_service/.env`.

Пример `auth_service/.env`:

```env
APP_NAME=auth-service
ENV=development
JWT_SECRET=change-me
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
SQLITE_PATH=./auth.db
```

Пример `bot_service/.env`:

```env
APP_NAME=bot-service
ENV=development
TELEGRAM_BOT_TOKEN=000000000:telegram-token
JWT_SECRET=change-me
JWT_ALG=HS256
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
OPENROUTER_API_KEY=sk-or-v1-example
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=http://localhost
OPENROUTER_APP_NAME=chat-application
```

Важно: `JWT_SECRET` и `JWT_ALG` в обоих сервисах должны совпадать, иначе бот не сможет валидировать токены, выданные Auth Service.

## Запуск через Docker Compose

Сначала соберите образы сервисов:

```bash
docker build -t auth-app:1.0 ./auth_service
docker build -t bot-app:1.0 ./bot_service
```

Затем запустите приложение:

```bash
docker compose up
```

После запуска доступны:

- Auth Service: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- RabbitMQ Management UI: `http://localhost:15672`
- RabbitMQ login/password по умолчанию: `guest` / `guest`

## API Auth Service

### Регистрация

`POST /auth/register`

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Ответ содержит публичные данные пользователя:

```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user"
}
```

### Авторизация

`POST /auth/login`

Маршрут использует `OAuth2PasswordRequestForm`, поэтому данные отправляются как form-data:

- `username` - email пользователя.
- `password` - пароль пользователя.

Ответ:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Текущий пользователь

`GET /auth/me`

Нужно передать JWT в заголовке:

```http
Authorization: Bearer <jwt>
```

## Работа с Telegram-ботом

1. Зарегистрируйтесь через `POST /auth/register`.
2. Получите JWT через `POST /auth/login`.
3. Откройте Telegram-бота.
4. Отправьте команду:

```text
/token <ваш_jwt_токен>
```

5. После успешного сохранения токена отправьте боту обычное текстовое сообщение.
6. Бот примет запрос в обработку, Celery worker отправит его в OpenRouter, а ответ придет отдельным сообщением.

Если токен отсутствует, истек или не проходит валидацию, бот попросит пройти авторизацию заново.

## Тестирование

Тесты разделены по сервисам.

Auth Service:

```bash
cd auth_service
uv run pytest
```

Bot Service:

```bash
cd bot_service
uv run pytest
```

## Скриншоты

### Swagger Auth Service

#### Регистрация
![Регистрация](images/auth_reg.png)
#### Авторизация
![Авторизация](images/auth_auth.png)
#### auth/me
![auth/me](images/auth_me.png)

### Telegram-бот

![telegram](images/tg_test.png)

### Инфраструктура и тесты

#### Rabbit
![rabbit](images/rabbit_test.png)
#### Тесты auth_service
![auth_service](images/auth_tests.png)
#### Тесты bot_service
![bot_service](images/bot_tests.png)
