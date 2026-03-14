from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from database import models  
from database.db import get_db
import logging
import traceback

#APIRouter — это способ группировать маршруты в FastAPI
router = APIRouter(tags=["routes"])
logger = logging.getLogger(__name__)

#Pydantic модели для проверки структуры ответов
#Описывают, как должен выглядеть каждый объект в списке
class HistoryResponse(BaseModel):
    id: int
    category_id: int
    category_name: str
    created_at: datetime
    status: str
    preview: str

class HistoryDetailResponse(HistoryResponse):
    attributes: dict
    generated_text: Optional[str] = None


#Получение списка запросов из истории
#response_model=List[HistoryResponse] — это указание FastAPI, как именно должны выглядеть данные, которые вернёт этот эндпоинт
@router.get("/history/", response_model=List[HistoryResponse])
def get_history(
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
    ):

    #Получаем список из таблицы запросов, подтягивая таблицы Категорий и Статусов
    query = db.query(models.Request).join(models.Category).join(models.Status)
    
    #Для фильтрации на сайте 
    if category:
        query = query.where(models.Category.name == category)
    if status:
        query = query.where(models.Status.name == status) 
    
    #Сортируем в порядке убывания
    requests = query.order_by(
        models.Request.created_at.desc()
    ).all()
    
    #Формируем список всех запросов
    result = []
    for req in requests:
        #Формируем название товара для отображения на сайте
        preview = get_preview(req, db)

        result.append({ #Формируем каждую отдельную запись и добавляем в список    
            "id": req.id,
            "category_id": req.category_id,
            "category_name": req.category_rel.name,
            "created_at": req.created_at,
            "status": req.status_rel.name,
            "preview": preview
        })
    
    return result

#Получение детальной информации о конкретном запросе
@router.get("/history/{request_id}", response_model=HistoryDetailResponse)
def get_request_detail(request_id: int, db: Session = Depends(get_db)):
    
    #Получаем запись из таблицы по id запроса
    request = db.query(models.Request).where(models.Request.id == request_id).first() 
    if not request:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    #Формирование словаря с характеристиками из БД в зависимости от категории
    attributes = {}
    #Подробная информация о телефоне
    if request.category_rel.name == 'phone':
        details = db.query(models.PhoneRequest).where(models.PhoneRequest.request_id == request_id).first() 
        if details:
            attributes = {
                "Бренд": details.brand,
                "Модель": details.model,
                "Диагональ экрана": f"{details.screen_size} Дюйм." if details.screen_size else "",
                "Тип матрицы": details.display_type,
                "Частота обновления": f"{details.screen_refresh} Гц" if details.screen_refresh else "",
                "ОС": details.os,
                "Сотовая связь": details.cellular,
                "Процессор": details.processor,
                "Память": f"{details.storage} Гб" if details.storage else "",
                "Камера": f"{details.camera} МП" if details.camera else "",
                "Батарея": f"{details.battery} мАч" if details.battery else "",
                "Зарядка": f"{details.charging_speed} Вт" if details.charging_speed else "",
                "Материал": details.material,
                "Вес": f"{details.weight} Гр" if details.weight else ""
            }
    #Подробная информации о ноутбуке
    elif request.category_rel.name == 'laptop':
        details = db.query(models.LaptopRequest).where(models.LaptopRequest.request_id == request_id).first() 
        if details:
            attributes = {
                "Бренд": details.brand,
                "Модель": details.model,
                "Диагональ экрана": f"{details.screen_size} Дюйм." if details.screen_size else "",
                "Тип матрицы": details.display_type,
                "Частота обновления": f"{details.screen_refresh} Гц" if details.screen_refresh else "",
                "Разрешение": details.screen_resolution,
                "Процессор": details.processor,
                "ОС": details.os,
                "RAM": f"{details.ram} Гб" if details.ram else "",
                "SSD": f"{details.ssd} Гб" if details.ssd else "",
                "Видеокарта": details.graphics_card,
                "VRAM": f"{details.vram} Гб" if details.vram else "",
                "Батарея": f"{details.battery} Вт/ч" if details.battery else "",
                "Блок питания": f"{details.power_adapter} Вт" if details.power_adapter else "",
                "Материал": details.material,
                "Вес": f"{details.weight} Кг" if details.weight else ""
            }
    #Подробная информации о телевизоре
    elif request.category_rel.name == 'tv':
        details = db.query(models.TvRequest).where(models.TvRequest.request_id == request_id).first() 
        if details:
            attributes = {
                "Бренд": details.brand,
                "Модель": details.model,
                "Диагональ экрана": f"{details.screen_size} Дюйм." if details.screen_size else "",
                "Тип матрицы": details.display_type,
                "Частота обновления": f"{details.screen_refresh} Гц" if details.screen_refresh else "",
                "Разрешение": details.screen_resolution,
                "Процессор": details.processor,
                "Мощность звука": f"{details.audio_power} Вт" if details.audio_power else "",
                "Аудиоканалы": details.speakers_channels,
                "Количество HDMI": f"{details.hdmi_count} Шт" if details.hdmi_count else "",
                "Версия HDMI": details.hdmi_version,
                "Установка": details.installation,
                "Материал": details.material,
                "Вес": f"{details.weight} Кг" if details.weight else ""
            }
    
    #Формируем название товара для отображения на сайте
    preview = get_preview(request, db)
    
    #Фильтруем пустые значения
    attributes = {k: v for k, v in attributes.items() if v}
    
    return { 
        "id": request.id,
        "category_id": request.category_id,
        "category_name": request.category_rel.name,
        "created_at": request.created_at,
        "status": request.status_rel.name,
        "generated_text": request.generated_text,
        "preview": preview,
        "attributes": attributes
    }

#Формирование "превью" для сайта (Бренд + Модель) 
def get_preview(request, db):

    #Если у запроса категория phone, то:
    if request.category_rel.name == 'phone':
        #Берем из таблицы запросов телефона запись, к которой относится основной запрос 
        details = db.query(models.PhoneRequest).where(models.PhoneRequest.request_id == request.id).first() 
        if details:
            #Возвращаем строку "Бренд + Модель" этой записи
            return f"{details.brand} {details.model}"
    
    #Аналогично для остальных категорий

    elif request.category_rel.name == 'laptop':
        details = db.query(models.LaptopRequest).where(models.LaptopRequest.request_id == request.id).first() 
        if details:
            return f"{details.brand} {details.model}"
    
    elif request.category_rel.name == 'tv':
        details = db.query(models.TvRequest).where(models.TvRequest.request_id == request.id).first() 
        if details:
            return f"{details.brand} {details.model}"
    
    return f"Запрос #{request.id}"

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