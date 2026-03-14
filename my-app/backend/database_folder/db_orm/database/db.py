from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/history.db"

#Создание движка - основное соединение с БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

#Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Функция получения сессии 
#Создаёт и автоматически закрывает сессию 
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

#Создание базового класса, от которого будут наследоваться все модели (таблицы)
Base = declarative_base()


