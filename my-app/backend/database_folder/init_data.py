from .db import execute_query
import logging

logger = logging.getLogger(__name__)

#Инициализация базы данных
def init_database():
    
    #Создание таблицы статусов
    execute_query("""
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """, commit=True)
    
    #Создание таблицы категорий
    execute_query("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """, commit=True)
    
    #Создание основной таблицы запросов
    execute_query("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            status_id INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            generated_text TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (status_id) REFERENCES statuses (id)
        )
    """, commit=True)
    
    #Создание таблицы для телефонов
    execute_query("""
        CREATE TABLE IF NOT EXISTS phone_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER UNIQUE NOT NULL,
            brand TEXT,
            model TEXT,
            screen_size TEXT,
            display_type TEXT,
            screen_refresh TEXT,
            processor TEXT,
            os TEXT,
            cellular TEXT,
            storage TEXT,
            camera TEXT,
            battery TEXT,
            charging_speed TEXT,
            material TEXT,
            weight TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (id) ON DELETE CASCADE
        )
    """, commit=True)
    
    #Создание таблицы для ноутбуков
    execute_query("""
        CREATE TABLE IF NOT EXISTS laptop_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER UNIQUE NOT NULL,
            brand TEXT,
            model TEXT,
            screen_size TEXT,
            display_type TEXT,
            screen_refresh TEXT,
            screen_resolution TEXT,
            processor TEXT,
            os TEXT,
            ram TEXT,
            ssd TEXT,
            graphics_card TEXT,
            vram TEXT,
            battery TEXT,
            power_adapter TEXT,
            material TEXT,
            weight TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (id) ON DELETE CASCADE
        )
    """, commit=True)
    
    #Создание таблицы для телевизоров
    execute_query("""
        CREATE TABLE IF NOT EXISTS tv_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER UNIQUE NOT NULL,
            brand TEXT,
            model TEXT,
            screen_size TEXT,
            display_type TEXT,
            screen_refresh TEXT,
            screen_resolution TEXT,
            processor TEXT,
            audio_power TEXT,
            speakers_channels TEXT,
            hdmi_count TEXT,
            hdmi_version TEXT,
            installation TEXT,
            material TEXT,
            weight TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (id) ON DELETE CASCADE
        )
    """, commit=True)
    
    #Добавление статусов, если их нет
    statuses = ["pending", "completed", "error"]
    for status in statuses:
        execute_query(
            "INSERT OR IGNORE INTO statuses (name) VALUES (?)",
            (status,),
            commit=True
        )
    
    #Добавление категорий, если их нет
    categories = ["phone", "laptop", "tv"]
    for category in categories:
        execute_query(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,),
            commit=True
        )
    
    #Исправляем существующие NULL записи, если они есть
    execute_query(
        "UPDATE requests SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL",
        commit=True
    )
    
    logger.info("База данных инициализирована")