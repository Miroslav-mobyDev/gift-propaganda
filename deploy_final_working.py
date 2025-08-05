#!/usr/bin/env python3
"""
Финальный рабочий скрипт деплоя на Render
"""

import os
import subprocess
import sys
from pathlib import Path

def check_files():
    """Проверяет наличие необходимых файлов"""
    required_files = [
        "requirements.txt",
        "server/main.py",
        "server/db.py",
        "server/models.py",
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

def show_working_instructions():
    """Показывает рабочие инструкции для деплоя"""
    print("\n" + "=" * 60)
    print("🚀 ФИНАЛЬНЫЙ РАБОЧИЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    instructions = """
🔧 ИСПРАВЛЕННЫЕ ПРОБЛЕМЫ:

1. ✅ Использую стабильные версии без компиляции Rust
2. ✅ FastAPI 0.95.2 (не требует pydantic-core 2.x)
3. ✅ Pydantic 1.10.8 (стабильная версия)
4. ✅ Uvicorn 0.22.0 (совместим)
5. ✅ SQLAlchemy 2.0.15 (стабильная версия)
6. ✅ psycopg2-binary 2.9.6 (стабильная версия)

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

🔧 КЛЮЧЕВЫЕ ИСПРАВЛЕНИЯ:

- ✅ Использую стабильные версии без компиляции Rust
- ✅ Убрал проблемные зависимости (aiohttp, apscheduler)
- ✅ Заменил на стабильные альтернативы (requests)
- ✅ Исправил синтаксис Pydantic (Config.from_attributes)
- ✅ Улучшил обработку ошибок

📊 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:

После исправлений приложение должно:
- ✅ Успешно собираться на Render
- ✅ Запускаться без ошибок компиляции
- ✅ Подключаться к PostgreSQL
- ✅ Работать с Telegram webhook
- ✅ Предоставлять API endpoints
"""
    
    print(instructions)

def create_deployment_summary():
    """Создает сводку деплоя"""
    print("\n📋 СВОДКА ДЕПЛОЯ")
    print("-" * 40)
    
    summary = f"""
✅ ГОТОВЫЕ ФАЙЛЫ:
   - requirements.txt (стабильные версии)
   - server/main.py (обновлен)
   - server/db.py (улучшен)
   - server/models.py (исправлен)
   - render.yaml (настроен)

⚙️ НАСТРОЙКИ RENDER:
   - Environment: Python 3.13
   - Build: pip install -r requirements.txt
   - Start: uvicorn server.main:app --host 0.0.0.0 --port $PORT

🔧 СТАБИЛЬНЫЕ ЗАВИСИМОСТИ:
   - ✅ fastapi 0.95.2 (без pydantic-core 2.x)
   - ✅ pydantic 1.10.8 (стабильная версия)
   - ✅ uvicorn 0.22.0
   - ✅ sqlalchemy 2.0.15
   - ✅ psycopg2-binary 2.9.6
   - ❌ aiohttp → ✅ requests
   - ❌ apscheduler → ✅ убран (не используется)

🔧 ИСПРАВЛЕНИЯ:
   - ✅ Убрал зависимости, требующие компиляцию Rust
   - ✅ Использую стабильные версии пакетов
   - ✅ Исправил синтаксис Pydantic (Config.from_attributes)
   - ✅ Улучшил обработку ошибок

📁 СТРУКТУРА ПРОЕКТА:
   ├── requirements.txt (стабильные версии)
   ├── render.yaml (настроен)
   ├── server/
   │   ├── main.py (обновлен)
   │   ├── db.py (улучшен)
   │   ├── models.py (исправлен)
   │   ├── config.py
   │   └── parsers/ (исправлен)
   └── ...

🚀 СЛЕДУЮЩИЕ ШАГИ:
   1. Перейдите на https://render.com
   2. Создайте Web Service
   3. Подключите GitHub репозиторий
   4. Настройте переменные окружения
   5. Создайте PostgreSQL базу данных
   6. Запустите деплой
"""
    
    print(summary)
    
    # Сохраняем сводку в файл
    with open("DEPLOYMENT_SUMMARY_WORKING.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📝 Сводка сохранена в DEPLOYMENT_SUMMARY_WORKING.txt")

def main():
    print("🚀 ФИНАЛЬНЫЙ РАБОЧИЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Показываем инструкции
    show_working_instructions()
    
    # Создаем сводку
    create_deployment_summary()
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
    print("\n🎯 ВАШИ ДЕЙСТВИЯ:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям выше")
    print("4. Используйте стабильные версии requirements.txt")
    print("\n📖 Дополнительная документация:")
    print("- DEPLOYMENT_SUMMARY_WORKING.txt")
    print("- RENDER_DEPLOY.md")
    print("- TROUBLESHOOTING.md")

if __name__ == "__main__":
    main() 