#!/usr/bin/env python3
"""
Простой тест для проверки основных компонентов
"""

import sys
import os

def test_basic_imports():
    """Тестирует базовые импорты"""
    print("🔍 Тестирование базовых импортов...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
        
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
        
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
        
        import requests
        print(f"✅ Requests {requests.__version__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_simple_app():
    """Создает простое FastAPI приложение"""
    print("\n🧪 Тестирование создания простого приложения...")
    
    try:
        from fastapi import FastAPI
        
        app = FastAPI()
        
        @app.get("/")
        def root():
            return {"message": "Hello World"}
        
        @app.get("/health")
        def health():
            return {"status": "ok"}
        
        print("✅ Простое FastAPI приложение создано")
        print(f"📊 Маршруты: {[route.path for route in app.routes]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        return False

def test_config():
    """Тестирует конфигурацию"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        # Проверяем переменные окружения
        database_url = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
        token = os.getenv('TOKEN', 'test_token')
        webhook_url = os.getenv('WEBHOOK_URL', 'https://test.com')
        
        print(f"✅ DATABASE_URL: {database_url[:50]}...")
        print(f"✅ TOKEN: {'SET' if token != 'test_token' else 'NOT SET'}")
        print(f"✅ WEBHOOK_URL: {webhook_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def main():
    print("🚀 ПРОСТОЙ ТЕСТ КОМПОНЕНТОВ")
    print("=" * 50)
    
    # Тестируем базовые импорты
    if not test_basic_imports():
        print("\n❌ Проблемы с базовыми импортами")
        return False
    
    # Тестируем создание приложения
    if not test_simple_app():
        print("\n❌ Проблемы с созданием приложения")
        return False
    
    # Тестируем конфигурацию
    if not test_config():
        print("\n❌ Проблемы с конфигурацией")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ВСЕ БАЗОВЫЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("\n🎯 Основные компоненты работают корректно")
    print("\n📋 Рекомендации для Render:")
    print("1. Используйте Python 3.11")
    print("2. Используйте обновленный requirements.txt")
    print("3. Start Command: uvicorn server.main:app --host 0.0.0.0 --port $PORT")
    
    return True

if __name__ == "__main__":
    main() 