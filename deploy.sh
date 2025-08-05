#!/bin/bash
# Автоматический деплой на Render

echo "🚀 Начинаем деплой на Render..."

# Проверяем, что все файлы на месте
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt не найден"
    exit 1
fi

if [ ! -f "server/main.py" ]; then
    echo "❌ server/main.py не найден"
    exit 1
fi

if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml не найден"
    exit 1
fi

echo "✅ Все файлы на месте"

# Коммитим изменения если есть
if ! git diff-index --quiet HEAD --; then
    echo "📝 Коммитим изменения..."
    git add .
    git commit -m "Auto deploy to Render"
fi

echo "✅ Готово к деплою!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Перейдите на https://render.com"
echo "2. Создайте новый Web Service"
echo "3. Подключите ваш GitHub репозиторий"
echo "4. Настройте переменные окружения:"
echo "   - TOKEN=your_telegram_bot_token"
echo "   - WEBHOOK_URL=https://your-app-name.onrender.com/webhook"
echo "5. Создайте PostgreSQL базу данных"
echo "6. Нажмите 'Create Web Service'"
