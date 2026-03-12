from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from database.db import execute_query
import logging
import traceback
from datetime import datetime

#APIRouter — это способ группировать маршруты в FastAPI
router = APIRouter(tags=["forms"])
logger = logging.getLogger(__name__)


#PHONE ROUTES
@router.post("/phone_form")
def phone_form(data: dict = Body()):
    logger.info(f"Получены данные для телефона: {data}")
    
    try:
        #Получаем id категории
        category = execute_query(
            "SELECT id FROM categories WHERE name = ?",
            ("phone",),
            fetch_one=True
        )
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        #Получаем id статуса
        status = execute_query(
            "SELECT id FROM statuses WHERE name = ?",
            ("pending",),
            fetch_one=True
        )
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        #Создаем запрос в основной таблице с явным указанием даты
        current_time = datetime.now().isoformat()
        request_id = execute_query(
            """
            INSERT INTO requests (category_id, status_id, created_at)
            VALUES (?, ?, ?)
            """,
            (category["id"], status["id"], current_time),
            commit=True
        )
        
        #Добавляем данные телефона
        execute_query(
            """
            INSERT INTO phone_requests (
                request_id, brand, model, screen_size, display_type,
                screen_refresh, processor, os, cellular, storage,
                camera, battery, charging_speed, material, weight
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                data.get("brand", ""),
                data.get("model", ""),
                data.get("screenSize", ""),
                data.get("matrixType", ""),
                data.get("frequency", ""),
                data.get("processor", ""),
                data.get("os", ""),
                data.get("cellular", ""),
                data.get("storage", ""),
                data.get("camera", ""),
                data.get("battery", ""),
                data.get("chargingSpeed", ""),
                data.get("material", ""),
                data.get("weight", "")
            ),
            commit=True
        )
        
        logger.info(f"Запрос #{request_id} для телефона успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": request_id}
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

### АНАЛОГИЧНО ДЛЯ ОСТАЛЬНЫХ ФОРМ ###

#LAPTOP ROUTES
@router.post("/laptop_form")
def laptop_form(data: dict = Body()):
    logger.info(f"Получены данные для ноутбука: {data}")
    
    try:
        category = execute_query(
            "SELECT id FROM categories WHERE name = ?",
            ("laptop",),
            fetch_one=True
        )
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        status = execute_query(
            "SELECT id FROM statuses WHERE name = ?",
            ("pending",),
            fetch_one=True
        )
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        current_time = datetime.now().isoformat()
        request_id = execute_query(
            """
            INSERT INTO requests (category_id, status_id, created_at)
            VALUES (?, ?, ?)
            """,
            (category["id"], status["id"], current_time),
            commit=True
        )
        
        execute_query(
            """
            INSERT INTO laptop_requests (
                request_id, brand, model, screen_size, display_type,
                screen_refresh, screen_resolution, processor, os,
                ram, ssd, graphics_card, vram, battery, power_adapter,
                material, weight
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                data.get("brand", ""),
                data.get("model", ""),
                data.get("diagonal", ""),
                data.get("matrix", ""),
                data.get("frequency", ""),
                data.get("resolution", ""),
                data.get("processor", ""),
                data.get("os", ""),
                data.get("ram", ""),
                data.get("ssd", ""),
                data.get("graphicsCard", ""),
                data.get("vram", ""),
                data.get("battery", ""),
                data.get("powerAdapter", ""),
                data.get("material", ""),
                data.get("weight", "")
            ),
            commit=True
        )
        
        logger.info(f"Запрос #{request_id} для ноутбука успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": request_id}
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

#TV ROUTES
@router.get("/tv_form")
def get_tv_form():
    return FileResponse("views/forms/tv_form.html")

@router.post("/tv_form")
def tv_form(data: dict = Body()):
    logger.info(f"Получены данные для телевизора: {data}")
    
    try:
        category = execute_query(
            "SELECT id FROM categories WHERE name = ?",
            ("tv",),
            fetch_one=True
        )
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        
        status = execute_query(
            "SELECT id FROM statuses WHERE name = ?",
            ("pending",),
            fetch_one=True
        )
        if not status:
            raise HTTPException(status_code=404, detail="Статус не найден")
        
        current_time = datetime.now().isoformat()
        request_id = execute_query(
            """
            INSERT INTO requests (category_id, status_id, created_at)
            VALUES (?, ?, ?)
            """,
            (category["id"], status["id"], current_time),
            commit=True
        )
        
        execute_query(
            """
            INSERT INTO tv_requests (
                request_id, brand, model, screen_size, display_type,
                screen_refresh, screen_resolution, processor,
                audio_power, speakers_channels, hdmi_count, hdmi_version,
                installation, material, weight
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                data.get("brand", ""),
                data.get("model", ""),
                data.get("screenSize", ""),
                data.get("matrixType", ""),
                data.get("frequency", ""),
                data.get("resolution", ""),
                data.get("processor", ""),
                data.get("audioPower", ""),
                data.get("numberOfSpeakers", ""),
                data.get("hdmiCount", ""),
                data.get("hdmiVersion", ""),
                data.get("installationMethod", ""),
                data.get("material", ""),
                data.get("weight", "")
            ),
            commit=True
        )
    
        logger.info(f"Запрос #{request_id} для телевизора успешно сохранен")
        return {"status": "success", "message": "Данные сохранены", "request_id": request_id}
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))