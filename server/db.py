# server/db.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news.db")

# Функция для создания движка с правильными настройками
def create_database_engine():
    """Создает движок базы данных с оптимальными настройками для Render"""
    if DATABASE_URL.startswith("sqlite"):
        # Для SQLite
        return create_engine(
            DATABASE_URL,
            echo=False,
            connect_args={"check_same_thread": False}
        )
    else:
        # Для PostgreSQL на Render
        # Обрабатываем URL для Render (может содержать ?sslmode=require)
        if "?" in DATABASE_URL:
            base_url = DATABASE_URL.split("?")[0]
        else:
            base_url = DATABASE_URL
        
        return create_engine(
            base_url,
            echo=False,
            # Настройки пула соединений для Render
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_reset_on_return='commit',
            # Настройки SSL для Render
            connect_args={
                "sslmode": "require",
                "connect_timeout": 30,
                "application_name": "giftpropaganda-api"
            }
        )

# Создаем движок базы данных
engine = create_database_engine()

# Сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NewsSource(Base):
    __tablename__ = 'news_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    url = Column(String(1000), nullable=False)
    source_type = Column(String(50), nullable=False)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class NewsItem(Base):
    __tablename__ = 'news_items'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('news_sources.id'), nullable=False)  # Жёсткая связь
    title = Column(String(1000), nullable=False)
    content = Column(Text, nullable=False)
    content_html = Column(Text, nullable=True)
    link = Column(String(1000), nullable=False)
    publish_date = Column(DateTime, nullable=False)
    category = Column(String(100), nullable=False)
    media = Column(JSON, nullable=True)
    image_url = Column(String(1000), nullable=True)
    video_url = Column(String(1000), nullable=True)
    reading_time = Column(Integer, nullable=True)
    views_count = Column(Integer, default=0)
    author = Column(String(200), nullable=True)
    subtitle = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source = relationship("NewsSource")  # Для удобного доступа

def get_db() -> Session:
    """Получает сессию базы данных с обработкой ошибок"""
    db = SessionLocal()
    try:
        # Проверяем соединение
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """Создает таблицы с обработкой ошибок"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы созданы успешно")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise


def get_db_session():
    """Получает сессию базы данных"""
    return SessionLocal()

def test_connection():
    """Тестирует подключение к базе данных"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно")
            return True
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False

def refresh_metadata():
    """Принудительно обновляет метаданные SQLAlchemy"""
    try:
        Base.metadata.reflect(bind=engine)
        logger.info("Метаданные SQLAlchemy обновлены")
    except Exception as e:
        logger.error(f"Ошибка при обновлении метаданных: {e}")

# Пересоздаем движок с обновленными метаданными
def recreate_engine():
    """Пересоздает движок базы данных с обновленными метаданными"""
    global engine, SessionLocal
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        refresh_metadata()
    except Exception as e:
        logger.warning(f"Не удалось обновить метаданные: {e}")
    return engine

# Пересоздаем модель с обновленными метаданными
def recreate_models():
    """Пересоздает модели с обновленными метаданными"""
    global NewsItem, NewsSource
    try:
        Base.metadata.reflect(bind=engine)
        return NewsItem, NewsSource
    except Exception as e:
        logger.error(f"Ошибка при пересоздании моделей: {e}")
        return NewsItem, NewsSource

# Инициализация при импорте
try:
    refresh_metadata()
except Exception as e:
    logger.warning(f"Ошибка при инициализации метаданных: {e}")
