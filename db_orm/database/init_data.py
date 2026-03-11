from database import models
from database.db import engine, get_db
import logging

logger = logging.getLogger(__name__)

#Инициализация базы данных
def init_database():

    db = get_db()

    try:
        #Создание БД
        models.Base.metadata.create_all(bind=engine)

        #Проверка при запуске сервера, что справочники в БД заполнены

        #Проверяем и добавляем статусы
        statuses = ["pending", "completed", "error"]
        for status_name in statuses:
            existing = db.query(models.Status).filter(models.Status.name == status_name).first()
            if not existing:
                db.add(models.Status(name=status_name))
                logger.info(f"Добавлен статус: {status_name}")
        
        #Проверяем и добавляем категории
        categories = ["phone", "laptop", "tv"]    
        for category_name in categories:
            existing = db.query(models.Category).filter(models.Category.name == category_name).first()
            if not existing:
                db.add(models.Category(name=category_name))
                logger.info(f"Добавлена категория: {category_name}")
        
        db.commit()
        logger.info("Справочники инициализированы")

    except Exception as e:
        logger.error(f"Ошибка инициализации: {e}")
        db.rollback()
    finally:
        db.close()
