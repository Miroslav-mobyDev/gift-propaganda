#!/usr/bin/env python3
"""
Автоматический деплой на Render с коммитом и пушем в GitHub
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

def check_git_status():
    """Проверяет статус Git и предлагает коммит"""
    print("🔍 Проверка Git статуса...")
    
    # Проверяем, есть ли изменения
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 Обнаружены изменения в репозитории:")
        print(result.stdout)
        
        # Предлагаем коммит
        response = input("\nХотите закоммитить изменения? (y/n): ").lower()
        if response == 'y':
            # Добавляем все файлы
            run_command("git add .")
            
            # Коммитим
            commit_message = input("Введите сообщение коммита (или нажмите Enter для авто): ").strip()
            if not commit_message:
                commit_message = "Auto deploy to Render"
            
            run_command(f'git commit -m "{commit_message}"')
            
            # Пушим
            push_response = input("Хотите запушить изменения в GitHub? (y/n): ").lower()
            if push_response == 'y':
                run_command("git push")
                print("✅ Изменения запушены в GitHub")
            else:
                print("⚠️  Не забудьте запушить изменения перед деплоем")
        else:
            print("⚠️  Рекомендуется закоммитить изменения перед деплоем")
    else:
        print("✅ Нет изменений для коммита")

def show_render_instructions():
    """Показывает инструкции для деплоя на Render"""
    print("\n" + "=" * 60)
    print("🚀 ИНСТРУКЦИИ ПО ДЕПЛОЮ НА RENDER")
    print("=" * 60)
    
    instructions = """
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
"""
    
    print(instructions)

def create_deploy_summary():
    """Создает краткую сводку для деплоя"""
    print("\n📋 КРАТКАЯ СВОДКА ДЕПЛОЯ")
    print("-" * 40)
    
    summary = f"""
✅ ГОТОВЫЕ ФАЙЛЫ:
   - requirements.txt ✓
   - server/main.py ✓
   - render.yaml ✓

⚙️ НАСТРОЙКИ RENDER:
   - Environment: Python
   - Build: pip install -r requirements.txt
   - Start: uvicorn server.main:app --host 0.0.0.0 --port $PORT

🔧 НЕОБХОДИМЫЕ ПЕРЕМЕННЫЕ:
   - TOKEN (ваш Telegram бот токен)
   - WEBHOOK_URL (https://your-app-name.onrender.com/webhook)
   - DATABASE_URL (создается автоматически)

📁 СТРУКТУРА ПРОЕКТА:
   ├── requirements.txt
   ├── render.yaml
   ├── server/
   │   ├── main.py
   │   ├── api/
   │   ├── models.py
   │   └── ...
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
    with open("DEPLOY_SUMMARY.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📝 Сводка сохранена в DEPLOY_SUMMARY.txt")

def main():
    print("🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА RENDER")
    print("=" * 60)
    
    # Проверяем Git статус
    check_git_status()
    
    # Показываем инструкции
    show_render_instructions()
    
    # Создаем сводку
    create_deploy_summary()
    
    print("\n" + "=" * 60)
    print("✅ ВСЕ ГОТОВО К ДЕПЛОЮ!")
    print("\n🎯 ВАШИ ДЕЙСТВИЯ:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте новый Web Service")
    print("3. Следуйте инструкциям выше")
    print("4. После деплоя обновите webhook в Telegram")
    print("\n📖 Дополнительная документация:")
    print("- RENDER_DEPLOY.md")
    print("- RENDER_DEPLOY_INSTRUCTIONS.txt")
    print("- DEPLOY_SUMMARY.txt")

if __name__ == "__main__":
    main() 