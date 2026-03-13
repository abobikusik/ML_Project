from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from database import models  
from database.db import get_db
import logging
import traceback

#APIRouter — это способ группировать маршруты в FastAPI
router = APIRouter(tags=["forms"])
logger = logging.getLogger(__name__)


#PHONE ROUTES
@router.post("/phone_form")
def phone_form(data: dict = Body()):

    logger.info(f"Получены данные для телефона: {data}")
    db = get_db()
    
    try:
        #Берем запись из таблицы Категорий, имя которой == phone 
        category = db.query(models.Category).where(models.Category.name == "phone").first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        #Берем запись из таблицы Статусов, имя которого == pending 
        status = db.query(models.Status).where(models.Status.name == "pending").first()
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        #Добавляем в основную таблицу Запросов id категории и статуса 
        db_request = models.Request(
            category_id=category.id,
            status_id=status.id
        )
        db.add(db_request)
        db.flush()
        
        #Формируем словарь на основе введенных пользователем данных для отправки в БД
        phone_data = {
            "brand": data.get("brand", ""),
            "model": data.get("model", ""),
            "screen_size": data.get("screenSize", ""),
            "display_type": data.get("matrixType", ""),
            "screen_refresh": data.get("frequency", ""),
            "processor": data.get("processor", ""),
            "os": data.get("os", ""),
            "cellular": data.get("cellular", ""),
            "storage": data.get("storage", ""),
            "camera": data.get("camera", ""),
            "battery": data.get("battery", ""),
            "charging_speed": data.get("chargingSpeed", ""),
            "material": data.get("material", ""),
            "weight": data.get("weight", "")
        }

        #Добавляем в таблицу Запросов Телефона id записи из таблицы Запросов, которая только что была добавлена, и данные, введенные пользователем
        db_phone = models.PhoneRequest(
            request_id=db_request.id,
            **phone_data #распаковка словаря 
        )
        db.add(db_phone)
        db.commit()
        
        logger.info(f"Запрос #{db_request.id} для телефона успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": db_request.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

### АНАЛОГИЧНО ДЛЯ ОСТАЛЬНЫХ ФОРМ ###

#LAPTOP ROUTES
@router.post("/laptop_form")
def laptop_form(data: dict = Body()):

    logger.info(f"Получены данные для ноутбука: {data}")
    db = get_db()
    
    try:
        category = db.query(models.Category).where(models.Category.name == "laptop").first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        status = db.query(models.Status).where(models.Status.name == "pending").first()
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        db_request = models.Request(
            category_id=category.id,
            status_id=status.id
        )
        db.add(db_request)
        db.flush()
        
        laptop_data = {
            "brand": data.get("brand", ""),
            "model": data.get("model", ""),
            "screen_size": data.get("diagonal", ""),
            "display_type": data.get("matrix", ""),
            "screen_refresh": data.get("frequency", ""),
            "screen_resolution": data.get("resolution", ""),
            "processor": data.get("processor", ""),
            "os": data.get("os", ""),
            "ram": data.get("ram", ""),
            "ssd": data.get("ssd", ""),
            "graphics_card": data.get("graphicsCard", ""),
            "vram": data.get("vram", ""),
            "battery": data.get("battery", ""),
            "power_adapter": data.get("powerAdapter", ""),
            "material": data.get("material", ""),
            "weight": data.get("weight", "")
        }  
        
        db_laptop = models.LaptopRequest(
            request_id=db_request.id,
            **laptop_data #распаковка словаря 
        )
        db.add(db_laptop)
        db.commit()
        
        logger.info(f"Запрос #{db_request.id} для ноутбука успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": db_request.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

#TV ROUTES
@router.post("/tv_form")
def tv_form(data: dict = Body()):

    logger.info(f"Получены данные для телевизора: {data}")
    db = get_db()
    
    try:
        category = db.query(models.Category).where(models.Category.name == "tv").first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        status = db.query(models.Status).where(models.Status.name == "pending").first()
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        db_request = models.Request(
            category_id=category.id,
            status_id=status.id
        )
        db.add(db_request)
        db.flush()
        
        tv_data = {
            "brand": data.get("brand", ""),
            "model": data.get("model", ""),
            "screen_size": data.get("screenSize", ""),
            "display_type": data.get("matrixType", ""),
            "screen_refresh": data.get("frequency", ""),
            "screen_resolution": data.get("resolution", ""),
            "processor": data.get("processor", ""),
            "audio_power": data.get("audioPower", ""),
            "speakers_channels": data.get("numberOfSpeakers", ""),
            "hdmi_count": data.get("hdmiCount", ""),
            "hdmi_version": data.get("hdmiVersion", ""),
            "installation": data.get("installationMethod", ""),
            "material": data.get("material", ""),
            "weight": data.get("weight", "")
        }
    
        db_tv = models.TvRequest(
            request_id=db_request.id,
            **tv_data #распаковка словаря 
        )
        db.add(db_tv)
        db.commit()
        
        logger.info(f"Запрос #{db_request.id} для телевизора успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": db_request.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()