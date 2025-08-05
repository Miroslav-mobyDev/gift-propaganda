#!/usr/bin/env python3
"""
Финальный скрипт для деплоя на Render с исправлениями
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении: {command}")
        print(f"Ошибка: {e.stderr}")
        return None

def check_files():
    """Проверяет наличие необходимых файлов"""
    required_files = [
        "requirements.txt",
        "server/main.py",
        "server/db.py",
        "render.yaml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Все необходимые файлы найдены")
    return True

def create_fixed_render_yaml():
    """Создает исправленный render.yaml"""
    print("🔧 Создание исправленного render.yaml...")
    
    render_config = """services:
  - type: web
    name: giftpropaganda-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn server.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: DATABASE_URL
        fromDatabase:
          name: giftpropaganda-db
          property: connectionString
"""
    
    with open("render.yaml", "w") as f:
        f.write(render_config)
    
    print("✅ render.yaml обновлен")

def create_database_service():
    """Создает конфигурацию для базы данных"""
    print("🗄️ Создание конфигурации базы данных...")
    
    db_config = """  - type: pserv
    name: giftpropaganda-db
    env: postgresql
    plan: free
    ipAllowList: []
"""
    
    # Добавляем конфигурацию БД в render.yaml
    with open("render.yaml", "r") as f:
        content = f.read()
    
    if "pserv" not in content:
        with open("render.yaml", "w") as f:
            f.write(content + "\n" + db_config)
        print("✅ Конфигурация базы данных добавлена")

def show_deploy_instructions():
    """Показывает инструкции для деплоя"""
    print("\n" + "=" * 60)
    print("🚀 ИСПРАВЛЕННЫЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    instructions = """
🔧 ИСПРАВЛЕНИЯ ПРОБЛЕМ С БАЗОЙ ДАННЫХ:

1. ✅ Улучшена обработка SSL соединений
2. ✅ Добавлены повторные попытки подключения
3. ✅ Улучшена обработка ошибок
4. ✅ Приложение не прерывается при ошибках БД
5. ✅ Добавлен детальный health check

📋 ПОШАГОВЫЕ ИНСТРУКЦИИ:

1. 🌐 ПЕРЕЙДИТЕ НА RENDER
   Ссылка: https://render.com

2. 📋 СОЗДАЙТЕ НОВЫЙ СЕРВИС
   - Нажмите "New +" → "Web Service"
   - Подключите ваш GitHub репозиторий
   - Выберите репозиторий GiftNews-main

3. ⚙️ НАСТРОЙТЕ СЕРВИС
   - Name: giftpropaganda-api
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn server.main:app --host 0.0.0.0 --port $PORT

4. 🔧 ДОБАВЬТЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
   В разделе "Environment Variables" добавьте:
   
   TOKEN=your_telegram_bot_token_here
   WEBHOOK_URL=https://your-app-name.onrender.com/webhook
   
   (DATABASE_URL создастся автоматически)

5. 🗄️ СОЗДАЙТЕ БАЗУ ДАННЫХ
   - Нажмите "New +" → "PostgreSQL"
   - Name: giftpropaganda-db
   - Подключите к вашему web сервису

6. 🚀 ЗАПУСТИТЕ ДЕПЛОЙ
   - Нажмите "Create Web Service"
   - Дождитесь завершения сборки (5-10 минут)

7. 🔗 ПОСЛЕ ДЕПЛОЯ
   - Обновите webhook в Telegram:
     https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook?url=https://your-app-name.onrender.com/webhook
   
   - Протестируйте API:
     https://your-app-name.onrender.com/health

8. ✅ ПРОВЕРЬТЕ РАБОТУ
   - Проверьте логи в Render Dashboard
   - Убедитесь, что бот отвечает на сообщения
   - Проверьте endpoint /health для диагностики

🔧 ДИАГНОСТИКА ПРОБЛЕМ:

Если возникают проблемы с БД:
1. Проверьте логи в Render Dashboard
2. Убедитесь, что PostgreSQL сервис запущен
3. Проверьте переменную DATABASE_URL
4. Попробуйте перезапустить сервис
5. Используйте endpoint /health для диагностики
"""
    
    print(instructions)

def create_troubleshooting_guide():
    """Создает руководство по устранению проблем"""
    print("📖 Создание руководства по устранению проблем...")
    
    guide = """# 🔧 РУКОВОДСТВО ПО УСТРАНЕНИЮ ПРОБЛЕМ

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
curl -X POST "https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.onrender.com/webhook"}'
```
"""
    
    with open("TROUBLESHOOTING.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("✅ Руководство по устранению проблем создано")

def main():
    print("🚀 ИСПРАВЛЕННЫЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Создаем исправленный render.yaml
    create_fixed_render_yaml()
    
    # Создаем конфигурацию базы данных
    create_database_service()
    
    # Показываем инструкции
    show_deploy_instructions()
    
    # Создаем руководство по устранению проблем
    create_troubleshooting_guide()
    
    print("\n" + "=" * 60)
    print("✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
    print("\n🎯 ВАШИ ДЕЙСТВИЯ:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям выше")
    print("4. При проблемах используйте TROUBLESHOOTING.md")
    print("\n📖 Дополнительная документация:")
    print("- TROUBLESHOOTING.md")
    print("- RENDER_DEPLOY.md")
    print("- test_db_connection.py")

if __name__ == "__main__":
    main() 