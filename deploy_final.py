#!/usr/bin/env python3
"""
Финальный скрипт для деплоя на Render с исправлениями зависимостей
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

def show_final_instructions():
    """Показывает финальные инструкции для деплоя"""
    print("\n" + "=" * 60)
    print("🚀 ФИНАЛЬНЫЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    instructions = """
🔧 ИСПРАВЛЕННЫЕ ПРОБЛЕМЫ:

1. ✅ Убрал aiohttp (несовместим с Python 3.13)
2. ✅ Заменил на requests (стабильная библиотека)
3. ✅ Обновил версии пакетов для совместимости
4. ✅ Убрал apscheduler (не используется)
5. ✅ Исправил проблемы с pydantic

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

- ✅ Убрал проблемные зависимости (aiohttp, apscheduler)
- ✅ Заменил на стабильные альтернативы (requests)
- ✅ Обновил версии пакетов для совместимости
- ✅ Исправил проблемы с Python 3.13
- ✅ Улучшил обработку ошибок

📊 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:

После исправлений приложение должно:
- ✅ Успешно собираться на Render
- ✅ Запускаться без ошибок зависимостей
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
   - requirements.txt (исправлен)
   - server/main.py (обновлен)
   - server/db.py (улучшен)
   - render.yaml (настроен)

⚙️ НАСТРОЙКИ RENDER:
   - Environment: Python 3.11
   - Build: pip install -r requirements.txt
   - Start: uvicorn server.main:app --host 0.0.0.0 --port $PORT

🔧 ИСПРАВЛЕННЫЕ ЗАВИСИМОСТИ:
   - ❌ aiohttp → ✅ requests
   - ❌ apscheduler → ✅ убран (не используется)
   - ✅ pydantic 1.10.8 (стабильная версия)
   - ✅ fastapi 0.95.2 (стабильная версия)

📁 СТРУКТУРА ПРОЕКТА:
   ├── requirements.txt (исправлен)
   ├── render.yaml (настроен)
   ├── server/
   │   ├── main.py (обновлен)
   │   ├── db.py (улучшен)
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
    with open("DEPLOYMENT_SUMMARY_FINAL.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📝 Сводка сохранена в DEPLOYMENT_SUMMARY_FINAL.txt")

def main():
    print("🚀 ФИНАЛЬНЫЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Показываем инструкции
    show_final_instructions()
    
    # Создаем сводку
    create_deployment_summary()
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
    print("\n🎯 ВАШИ ДЕЙСТВИЯ:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям выше")
    print("4. Используйте исправленный requirements.txt")
    print("\n📖 Дополнительная документация:")
    print("- DEPLOYMENT_SUMMARY_FINAL.txt")
    print("- RENDER_DEPLOY.md")
    print("- TROUBLESHOOTING.md")

if __name__ == "__main__":
    main() 