# 🔧 РУКОВОДСТВО ПО УСТРАНЕНИЮ ПРОБЛЕМ

## Проблема: Ошибка подключения к базе данных

### Симптомы:
- "SSL connection has been closed unexpectedly"
- "connection to server failed"
- Приложение не запускается

### Решения:

1. **Проверьте PostgreSQL сервис**
   - Убедитесь, что PostgreSQL сервис запущен
   - Проверьте статус в Render Dashboard

2. **Проверьте переменные окружения**
   - DATABASE_URL должен быть автоматически создан
   - Убедитесь, что TOKEN и WEBHOOK_URL установлены

3. **Перезапустите сервисы**
   - Перезапустите PostgreSQL сервис
   - Перезапустите Web сервис

4. **Проверьте логи**
   - В Render Dashboard → Logs
   - Ищите ошибки подключения к БД

5. **Используйте диагностику**
   - Проверьте endpoint /health
   - Запустите test_db_connection.py локально

## Проблема: Webhook не работает

### Решения:
1. Убедитесь, что TOKEN правильный
2. Проверьте WEBHOOK_URL
3. Обновите webhook вручную:
   ```
   https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook?url=https://your-app-name.onrender.com/webhook
   ```

## Проблема: Приложение не отвечает

### Решения:
1. Проверьте логи в Render Dashboard
2. Убедитесь, что порт указан правильно
3. Проверьте Build Command и Start Command
4. Убедитесь, что все зависимости установлены

## Полезные команды:

### Локальное тестирование:
```bash
python test_db_connection.py
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### Проверка состояния:
```bash
curl https://your-app-name.onrender.com/health
```

### Обновление webhook:
```bash
curl -X POST "https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook"      -H "Content-Type: application/json"      -d '{"url": "https://your-app-name.onrender.com/webhook"}'
```
