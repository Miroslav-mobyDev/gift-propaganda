#!/usr/bin/env python3
"""
Скрипт для тестирования подключения к базе данных
"""

import os
import sys
import time
from pathlib import Path

# Добавляем путь к серверу
sys.path.append(str(Path(__file__).parent / "server"))

from server.db import test_connection, create_database_engine, engine

def test_database_connection():
    """Тестирует подключение к базе данных"""
    print("🔍 Тестирование подключения к базе данных...")
    
    # Проверяем переменные окружения
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL не установлен")
        return False
    
    # Обрезаем URL для безопасности
    safe_url = database_url.split('@')[0] + '@***' if '@' in database_url else database_url
    print(f"📊 DATABASE_URL: {safe_url}")
    
    # Тестируем подключение
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 Попытка {attempt}/{max_attempts}...")
        
        try:
            if test_connection():
                print("✅ Подключение к базе данных успешно!")
                return True
            else:
                print("❌ Тест подключения не прошел")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
        
        if attempt < max_attempts:
            wait_time = 3 * attempt
            print(f"⏳ Ожидание {wait_time} секунд...")
            time.sleep(wait_time)
    
    print("❌ Не удалось подключиться к базе данных")
    return False

def test_database_operations():
    """Тестирует операции с базой данных"""
    print("\n🧪 Тестирование операций с базой данных...")
    
    try:
        from server.db import get_db_session, NewsSource, NewsItem
        
        # Создаем сессию
        db = get_db_session()
        
        # Тестируем простой запрос
        result = db.execute("SELECT 1 as test")
        row = result.fetchone()
        if row and row[0] == 1:
            print("✅ Простой запрос выполнен успешно")
        else:
            print("❌ Ошибка при выполнении простого запроса")
            return False
        
        # Тестируем запрос к таблицам
        try:
            sources_count = db.query(NewsSource).count()
            print(f"✅ Запрос к таблице news_sources: {sources_count} записей")
        except Exception as e:
            print(f"⚠️  Ошибка при запросе к news_sources: {e}")
        
        try:
            items_count = db.query(NewsItem).count()
            print(f"✅ Запрос к таблице news_items: {items_count} записей")
        except Exception as e:
            print(f"⚠️  Ошибка при запросе к news_items: {e}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании операций: {e}")
        return False

def main():
    print("🚀 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
    print("=" * 50)
    
    # Тестируем подключение
    if test_database_connection():
        print("\n✅ Подключение к базе данных работает!")
        
        # Тестируем операции
        if test_database_operations():
            print("\n✅ Все тесты пройдены успешно!")
        else:
            print("\n⚠️  Есть проблемы с операциями базы данных")
    else:
        print("\n❌ Проблемы с подключением к базе данных")
        print("\n🔧 Рекомендации:")
        print("1. Проверьте DATABASE_URL в переменных окружения")
        print("2. Убедитесь, что база данных PostgreSQL создана на Render")
        print("3. Проверьте настройки SSL в Render Dashboard")
        print("4. Попробуйте перезапустить сервис на Render")

if __name__ == "__main__":
    main() 