#!/usr/bin/env python3
"""
Быстрый деплой на Render
"""

import os
import subprocess
import sys
from pathlib import Path

def print_step(step, description):
    """Выводит шаг с описанием"""
    print(f"\n{step} {description}")
    print("-" * 50)

def check_prerequisites():
    """Проверяет предварительные требования"""
    print_step("🔍", "Проверка требований")
    
    # Проверяем файлы
    required_files = ["requirements.txt", "server/main.py", "render.yaml"]
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - ОТСУТСТВУЕТ!")
            return False
    
    # Проверяем Git
    try:
        result = subprocess.run("git status", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git репозиторий")
        else:
            print("❌ Git репозиторий не найден")
            return False
    except:
        print("❌ Ошибка проверки Git")
        return False
    
    return True

def create_deploy_script():
    """Создает скрипт для автоматического деплоя"""
    print_step("📝", "Создание скрипта деплоя")
    
    script_content = """#!/bin/bash
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
"""
    
    with open("deploy.sh", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Скрипт deploy.sh создан")

def show_render_config():
    """Показывает конфигурацию для Render"""
    print_step("⚙️", "Конфигурация Render")
    
    print("render.yaml:")
    with open("render.yaml", "r") as f:
        print(f.read())
    
    print("\nrequirements.txt:")
    with open("requirements.txt", "r") as f:
        print(f.read())

def create_env_template():
    """Создает шаблон .env файла"""
    print_step("🔧", "Создание шаблона переменных окружения")
    
    env_template = """# Переменные окружения для Render
# Скопируйте эти значения в Render Dashboard

# Telegram Bot Token
TOKEN=your_telegram_bot_token_here

# Webhook URL (замените на ваш URL после деплоя)
WEBHOOK_URL=https://your-app-name.onrender.com/webhook

# Database URL (создается автоматически в Render)
DATABASE_URL=postgresql://...
"""
    
    with open(".env.template", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("✅ .env.template создан")

def show_deploy_checklist():
    """Показывает чек-лист для деплоя"""
    print_step("📋", "Чек-лист деплоя")
    
    checklist = """
✅ ПОДГОТОВКА:
   □ Код закоммичен в GitHub
   □ Все файлы на месте
   □ render.yaml настроен
   □ requirements.txt обновлен

🌐 RENDER DASHBOARD:
   □ Создан аккаунт на render.com
   □ Подключен GitHub репозиторий
   □ Создан Web Service
   □ Настроены переменные окружения
   □ Создана PostgreSQL база данных

⚙️ НАСТРОЙКИ СЕРВИСА:
   □ Name: giftpropaganda-api
   □ Environment: Python
   □ Build Command: pip install -r requirements.txt
   □ Start Command: uvicorn server.main:app --host 0.0.0.0 --port $PORT

🔧 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ:
   □ TOKEN=your_telegram_bot_token
   □ WEBHOOK_URL=https://your-app-name.onrender.com/webhook
   □ DATABASE_URL=postgresql://... (автоматически)

🚀 ДЕПЛОЙ:
   □ Нажат "Create Web Service"
   □ Сборка завершена успешно
   □ Сервис запущен

🔗 ПОСЛЕ ДЕПЛОЯ:
   □ Обновлен webhook в Telegram
   □ Протестирован API
   □ Проверены логи
"""
    
    print(checklist)

def main():
    print("🚀 БЫСТРЫЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    # Проверяем требования
    if not check_prerequisites():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Создаем скрипт деплоя
    create_deploy_script()
    
    # Показываем конфигурацию
    show_render_config()
    
    # Создаем шаблон .env
    create_env_template()
    
    # Показываем чек-лист
    show_deploy_checklist()
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ГОТОВО К ДЕПЛОЮ!")
    print("\n📋 Выполните следующие действия:")
    print("1. Запустите: bash deploy.sh")
    print("2. Перейдите на https://render.com")
    print("3. Следуйте чек-листу выше")
    print("\n📖 Подробная документация: RENDER_DEPLOY.md")

if __name__ == "__main__":
    main() 