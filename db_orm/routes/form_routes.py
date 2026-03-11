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
@router.get("/phone_form")
def get_phone_form():
    return FileResponse("views/forms/phone_form.html")

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
            "screen_size": data.get("screen_size", ""),
            "display_type": data.get("display_type", ""),
            "screen_refresh": data.get("screen_refresh", ""),
            "processor": data.get("processor", ""),
            "os": data.get("OS", ""),
            "cellular": data.get("cellular", ""),
            "storage": data.get("storage", ""),
            "camera": data.get("camera", ""),
            "battery": data.get("battery", ""),
            "charging_speed": data.get("charging_speed", ""),
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
@router.get("/laptop_form")
def get_laptop_form():
    return FileResponse("views/forms/laptop_form.html")

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
            "screen_size": data.get("screen_size", ""),
            "display_type": data.get("display_type", ""),
            "screen_refresh": data.get("screen_refresh", ""),
            "screen_resolution": data.get("screen_resolution", ""),
            "processor": data.get("processor", ""),
            "os": data.get("OS", ""),
            "ram": data.get("RAM", ""),
            "ssd": data.get("SSD", ""),
            "graphics_card": data.get("graphics_card", ""),
            "vram": data.get("VRAM", ""),
            "battery": data.get("battery", ""),
            "power_adapter": data.get("power_adapter", ""),
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
@router.get("/tv_form")
def get_tv_form():
    return FileResponse("views/forms/tv_form.html")

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
            "screen_size": data.get("screen_size", ""),
            "display_type": data.get("display_type", ""),
            "screen_refresh": data.get("screen_refresh", ""),
            "screen_resolution": data.get("screen_resolution", ""),
            "processor": data.get("processor", ""),
            "os": data.get("OS", ""),
            "audio_power": data.get("audio_power", ""),
            "speakers_channels": data.get("speakers_channels", ""),
            "hdmi_count": data.get("HDMI_count", ""),
            "installation": data.get("installation", ""),
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