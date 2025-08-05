#!/usr/bin/env python3
"""
Автоматический скрипт для деплоя на Render
"""

import os
import subprocess
import sys
import requests
import json
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

def check_git_status():
    """Проверяет статус Git репозитория"""
    try:
        # Проверяем, что мы в Git репозитории
        result = subprocess.run(
            "git status",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Не найден Git репозиторий")
            return False
        
        # Проверяем, есть ли изменения
        if "nothing to commit" not in result.stdout:
            print("⚠️  Есть незакоммиченные изменения")
            print("Рекомендуется сделать коммит перед деплоем")
            return False
        
        print("✅ Git репозиторий в порядке")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке Git: {e}")
        return False

def check_environment_variables():
    """Проверяет наличие переменных окружения"""
    required_vars = ['TOKEN', 'WEBHOOK_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Отсутствуют переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nЭти переменные нужно будет настроить в Render Dashboard")
        return False
    
    print("✅ Переменные окружения настроены")
    return True

def test_local_server():
    """Тестирует локальный сервер"""
    print("🧪 Тестирование локального сервера...")
    
    try:
        # Запускаем сервер в фоне
        process = subprocess.Popen(
            "python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Ждем немного для запуска
        import time
        time.sleep(3)
        
        # Тестируем endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Локальный сервер работает корректно")
            process.terminate()
            return True
        else:
            print(f"❌ Ошибка сервера: {response.status_code}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании сервера: {e}")
        return False

def create_deploy_instructions():
    """Создает инструкции для деплоя"""
    instructions = """
🚀 ИНСТРУКЦИИ ПО ДЕПЛОЮ НА RENDER

1. 📋 ПОДГОТОВКА
   - Убедитесь, что код закоммичен в GitHub
   - Проверьте, что все файлы на месте

2. 🌐 СОЗДАНИЕ СЕРВИСА НА RENDER
   - Перейдите на https://render.com
   - Нажмите "New +" → "Web Service"
   - Подключите ваш GitHub репозиторий

3. ⚙️ НАСТРОЙКА СЕРВИСА
   - Name: giftpropaganda-api
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn server.main:app --host 0.0.0.0 --port $PORT

4. 🔧 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
   Добавьте в Render Dashboard:
   - TOKEN=your_telegram_bot_token
   - WEBHOOK_URL=https://your-app-name.onrender.com/webhook
   - DATABASE_URL=postgresql://... (создается автоматически)

5. 🗄️ СОЗДАНИЕ БАЗЫ ДАННЫХ
   - Нажмите "New +" → "PostgreSQL"
   - Name: giftpropaganda-db
   - Подключите к вашему web сервису

6. 🚀 ДЕПЛОЙ
   - Нажмите "Create Web Service"
   - Дождитесь завершения сборки

7. 🔗 НАСТРОЙКА WEBHOOK
   После деплоя обновите webhook:
   https://api.telegram.org/bot{YOUR_TOKEN}/setWebhook?url=https://your-app-name.onrender.com/webhook

8. ✅ ПРОВЕРКА
   - Проверьте логи в Render Dashboard
   - Тестируйте API: https://your-app-name.onrender.com/health
"""
    
    with open("RENDER_DEPLOY_INSTRUCTIONS.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📝 Инструкции сохранены в RENDER_DEPLOY_INSTRUCTIONS.txt")

def main():
    print("🚀 ПОДГОТОВКА К ДЕПЛОЮ НА RENDER")
    print("=" * 50)
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Исправьте ошибки и запустите скрипт снова")
        sys.exit(1)
    
    # Проверяем Git
    check_git_status()
    
    # Проверяем переменные окружения
    check_environment_variables()
    
    # Тестируем локальный сервер
    test_local_server()
    
    # Создаем инструкции
    create_deploy_instructions()
    
    print("\n" + "=" * 50)
    print("✅ ПРОЕКТ ГОТОВ К ДЕПЛОЮ!")
    print("\n📋 Следующие шаги:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям в RENDER_DEPLOY_INSTRUCTIONS.txt")
    print("\n📖 Подробная документация: RENDER_DEPLOY.md")

if __name__ == "__main__":
    main() 