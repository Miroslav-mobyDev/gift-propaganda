#!/usr/bin/env python3
"""
Скрипт деплоя с исправлениями для версии Python
"""

import os
import subprocess
import sys
from pathlib import Path

def check_files():
    """Проверяет наличие необходимых файлов"""
    required_files = [
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "runtime.txt",
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

def show_python_fix_instructions():
    """Показывает инструкции с исправлениями для версии Python"""
    print("\n" + "=" * 60)
    print("🚀 ДЕПЛОЙ С ИСПРАВЛЕНИЯМИ ВЕРСИИ PYTHON")
    print("=" * 60)
    
    instructions = """
🔧 ИСПРАВЛЕННЫЕ ПРОБЛЕМЫ:

1. ✅ Создал pyproject.toml с ограничением Python >=3.11,<3.12
2. ✅ Создал setup.py для дополнительной совместимости
3. ✅ Создал runtime.txt для явного указания версии Python
4. ✅ Обновил render.yaml для использования pyproject.toml
5. ✅ Ограничил версию Python до 3.11.x (не 3.13)

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
   - Build Command: pip install -e .
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

- ✅ Ограничил версию Python до 3.11.x
- ✅ Использую pyproject.toml для управления зависимостями
- ✅ Создал setup.py для дополнительной совместимости
- ✅ Добавил runtime.txt для явного указания версии Python
- ✅ Обновил build command в render.yaml

📊 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:

После исправлений приложение должно:
- ✅ Использовать Python 3.11 (не 3.13)
- ✅ Успешно собираться на Render
- ✅ Запускаться без ошибок Pydantic
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
   - pyproject.toml (новый - ограничение Python)
   - setup.py (новый - совместимость)
   - runtime.txt (новый - версия Python)
   - server/main.py (обновлен)
   - server/db.py (улучшен)
   - server/models.py (исправлен)
   - render.yaml (обновлен)

⚙️ НАСТРОЙКИ RENDER:
   - Environment: Python 3.11 (ограничено)
   - Build: pip install -e .
   - Start: uvicorn server.main:app --host 0.0.0.0 --port $PORT

🔧 ИСПРАВЛЕНИЯ ВЕРСИИ PYTHON:
   - ✅ pyproject.toml: requires-python = ">=3.11,<3.12"
   - ✅ setup.py: python_requires=">=3.11,<3.12"
   - ✅ runtime.txt: python-3.11.0
   - ✅ render.yaml: buildCommand: pip install -e .

🔧 СТАБИЛЬНЫЕ ЗАВИСИМОСТИ:
   - ✅ fastapi 0.95.2 (совместим с Python 3.11)
   - ✅ pydantic 1.10.8 (совместим с Python 3.11)
   - ✅ uvicorn 0.22.0
   - ✅ sqlalchemy 2.0.15
   - ✅ psycopg2-binary 2.9.6

📁 СТРУКТУРА ПРОЕКТА:
   ├── requirements.txt (стабильные версии)
   ├── pyproject.toml (новый)
   ├── setup.py (новый)
   ├── runtime.txt (новый)
   ├── render.yaml (обновлен)
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
    with open("DEPLOYMENT_SUMMARY_PYTHON_FIX.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📝 Сводка сохранена в DEPLOYMENT_SUMMARY_PYTHON_FIX.txt")

def main():
    print("🚀 ДЕПЛОЙ С ИСПРАВЛЕНИЯМИ ВЕРСИИ PYTHON")
    print("=" * 60)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Показываем инструкции
    show_python_fix_instructions()
    
    # Создаем сводку
    create_deployment_summary()
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
    print("\n🎯 ВАШИ ДЕЙСТВИЯ:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям выше")
    print("4. Используйте новые файлы конфигурации")
    print("\n📖 Дополнительная документация:")
    print("- DEPLOYMENT_SUMMARY_PYTHON_FIX.txt")
    print("- RENDER_DEPLOY.md")
    print("- TROUBLESHOOTING.md")

if __name__ == "__main__":
    main() 