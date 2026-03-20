import sqlite3
import os
from contextlib import contextmanager

DATABASE = os.getenv("DATABASE_PATH", "./database/history.db")

def get_db_connection():
    #Получить соединение с БД
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  #чтобы получать результаты как словари
    return conn

@contextmanager
def get_db():
    #Контекстный менеджер для работы с БД
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    #Универсальная функция для выполнения SQL запросов
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if commit:
            conn.commit()
            # Если это INSERT, возвращаем lastrowid
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            # Для UPDATE/DELETE возвращаем rowcount
            return cursor.rowcount
        
        if fetch_one:
            result = cursor.fetchone()
            return dict(result) if result else None
        
        if fetch_all:
            results = cursor.fetchall()
            return [dict(row) for row in results]
        
        return cursor