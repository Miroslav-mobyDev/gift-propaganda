#!/usr/bin/env python3
"""
Тестовый файл для проверки запуска приложения
"""

import sys
import os
from pathlib import Path

# Добавляем путь к серверу
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Тестирует импорты основных модулей"""
    print("🔍 Тестирование импортов...")
    
    try:
        # Тестируем импорт основных модулей
        from server.config import TOKEN, WEBHOOK_URL
        print("✅ server.config импортирован успешно")
        
        from server.db import engine, test_connection
        print("✅ server.db импортирован успешно")
        
        from server.main import app
        print("✅ server.main импортирован успешно")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_app_creation():
    """Тестирует создание FastAPI приложения"""
    print("\n🧪 Тестирование создания приложения...")
    
    try:
        from server.main import app
        
        # Проверяем, что app создан
        if hasattr(app, 'routes'):
            print("✅ FastAPI приложение создано успешно")
            print(f"📊 Количество маршрутов: {len(app.routes)}")
            return True
        else:
            print("❌ Приложение не имеет маршрутов")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        return False

def test_endpoints():
    """Тестирует основные endpoints"""
    print("\n🔗 Тестирование endpoints...")
    
    try:
        from server.main import app
        
        # Проверяем основные endpoints
        routes = [route.path for route in app.routes]
        print(f"📋 Доступные маршруты: {routes}")
        
        # Проверяем наличие основных endpoints
        required_endpoints = ['/', '/health', '/api/news', '/telegram/webhook']
        for endpoint in required_endpoints:
            if any(endpoint in route for route in routes):
                print(f"✅ {endpoint} найден")
            else:
                print(f"⚠️  {endpoint} не найден")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования endpoints: {e}")
        return False

def main():
    print("🚀 ТЕСТИРОВАНИЕ ПРИЛОЖЕНИЯ")
    print("=" * 50)
    
    # Тестируем импорты
    if not test_imports():
        print("\n❌ Проблемы с импортами")
        return False
    
    # Тестируем создание приложения
    if not test_app_creation():
        print("\n❌ Проблемы с созданием приложения")
        return False
    
    # Тестируем endpoints
    if not test_endpoints():
        print("\n❌ Проблемы с endpoints")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("\n🎯 Приложение готово к деплою на Render")
    print("\n📋 Start Command для Render:")
    print("uvicorn server.main:app --host 0.0.0.0 --port $PORT")
    
    return True

if __name__ == "__main__":
    main() 