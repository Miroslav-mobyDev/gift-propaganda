# 🚀 Простой деплой на Render

## Шаг 1: Создание сервиса на Render

1. Перейдите на [render.com](https://render.com)
2. Нажмите **"New +"** → **"Web Service"**
3. Подключите ваш GitHub репозиторий

## Шаг 2: Настройка сервиса

### Основные настройки:
- **Name**: `giftpropaganda-api`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`

## Шаг 3: Создание базы данных

1. Нажмите **"New +"** → **"PostgreSQL"**
2. Настройте:
   - **Name**: `giftpropaganda-db`
   - **Database**: `giftpropaganda`
   - **User**: `giftpropaganda`

## Шаг 4: Переменные окружения

В настройках web сервиса добавьте:

```
DATABASE_URL=postgresql://user:password@host:port/database
TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://your-app-name.onrender.com/webhook
```

## Шаг 5: Деплой

1. Нажмите **"Create Web Service"**
2. Render автоматически задеплоит ваше приложение

## 🔧 Проверка

После деплоя проверьте:
- `https://your-app-name.onrender.com/health`
- Логи в разделе "Logs"

## 📱 Настройка бота

```python
import requests

url = f"https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook"
data = {"url": "https://your-app-name.onrender.com/webhook"}
response = requests.post(url, json=data)
print(response.json())
``` 