from fastapi import APIRouter, HTTPException, Body
from database.db import execute_query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
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
    status: Optional[str] = None
    ):
    
    #Получаем список из таблицы запросов, подтягивая таблицы Категорий и Статусов
    query = """
        SELECT 
            r.id, r.category_id, r.created_at,
            c.name as category_name,
            s.name as status
        FROM requests r
        JOIN categories c ON r.category_id = c.id
        JOIN statuses s ON r.status_id = s.id
        WHERE 1=1
    """
    params = []
    
    #Для фильтрации на сайте 
    if category:
        query += " AND c.name = ?"
        params.append(category)
    if status:
        query += " AND s.name = ?"
        params.append(status)
    
    #Сортируем в порядке убывания
    query += " ORDER BY r.created_at DESC"
    requests = execute_query(query, params, fetch_all=True)
    
    #Формируем список всех запросов
    result = []
    for req in requests:
        #Формируем название товара для отображения на сайте
        preview = get_preview(req["id"], req["category_name"])

        result.append({
            "id": req["id"],
            "category_id": req["category_id"],
            "category_name": req["category_name"],
            "created_at": req["created_at"],
            "status": req["status"],
            "preview": preview
        })
    
    return result

@router.get("/history/{request_id}", response_model=HistoryDetailResponse)
def get_request_detail(request_id: int):
    
    #Получаем основной запрос
    request = execute_query(
        """
        SELECT 
            r.id, r.category_id, r.created_at, r.generated_text,
            c.name as category_name,
            s.name as status
        FROM requests r
        JOIN categories c ON r.category_id = c.id
        JOIN statuses s ON r.status_id = s.id
        WHERE r.id = ?
        """,
        (request_id,),
        fetch_one=True
    )
    
    if not request:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    #Получаем детали в зависимости от категории
    attributes = {}
    #Подробная информация о телефоне
    if request["category_name"] == 'phone':
        details = execute_query(
            "SELECT * FROM phone_requests WHERE request_id = ?",
            (request_id,),
            fetch_one=True
        )
        if details:
            attributes = {
                "Бренд": details["brand"],
                "Модель": details["model"],
                "Диагональ экрана": f"{details['screen_size']} Дюйм." if details["screen_size"] else "",
                "Тип матрицы": details["display_type"],
                "Частота обновления": f"{details['screen_refresh']} Гц" if details["screen_refresh"] else "",
                "ОС": details["os"],
                "Сотовая связь": details["cellular"],
                "Процессор": details["processor"],
                "Память": f"{details['storage']} Гб" if details["storage"] else "",
                "Камера": f"{details['camera']} МП" if details["camera"] else "",
                "Батарея": f"{details['battery']} мАч" if details["battery"] else "",
                "Зарядка": f"{details['charging_speed']} Вт" if details["charging_speed"] else "",
                "Материал": details["material"],
                "Вес": f"{details['weight']} Гр" if details["weight"] else ""
            }
    #Подробная информации о ноутбуке
    elif request["category_name"] == 'laptop':
        details = execute_query(
            "SELECT * FROM laptop_requests WHERE request_id = ?",
            (request_id,),
            fetch_one=True
        )
        if details:
            attributes = {
                "Бренд": details["brand"],
                "Модель": details["model"],
                "Диагональ экрана": f"{details['screen_size']} Дюйм." if details["screen_size"] else "",
                "Тип матрицы": details["display_type"],
                "Частота обновления": f"{details['screen_refresh']} Гц" if details["screen_refresh"] else "",
                "Разрешение": details["screen_resolution"],
                "Процессор": details["processor"],
                "ОС": details["os"],
                "RAM": f"{details['ram']} Гб" if details["ram"] else "",
                "SSD": f"{details['ssd']} Гб" if details["ssd"] else "",
                "Видеокарта": details["graphics_card"],
                "VRAM": f"{details['vram']} Гб" if details["vram"] else "",
                "Батарея": f"{details['battery']} Вт/ч" if details["battery"] else "",
                "Блок питания": f"{details['power_adapter']} Вт" if details["power_adapter"] else "",
                "Материал": details["material"],
                "Вес": f"{details['weight']} Кг" if details["weight"] else ""
            }
    #Подробная информации о телевизоре
    elif request["category_name"] == 'tv':
        details = execute_query(
            "SELECT * FROM tv_requests WHERE request_id = ?",
            (request_id,),
            fetch_one=True
        )
        if details:
            attributes = {
                "Бренд": details["brand"],
                "Модель": details["model"],
                "Диагональ экрана": f"{details['screen_size']} Дюйм." if details["screen_size"] else "",
                "Тип матрицы": details["display_type"],
                "Частота обновления": f"{details['screen_refresh']} Гц" if details["screen_refresh"] else "",
                "Разрешение": details["screen_resolution"],
                "Процессор": details["processor"],
                "ОС": details["os"],
                "Мощность звука": f"{details['audio_power']} Вт" if details["audio_power"] else "",
                "Аудиоканалы": details["speakers_channels"],
                "Количество HDMI": f"{details['hdmi_count']} Шт" if details["hdmi_count"] else "",
                "Версия HDMI": details['hdmi_version'],
                "Установка": details["installation"],
                "Материал": details["material"],
                "Вес": f"{details['weight']} Кг" if details["weight"] else ""
            }
    
    #Формируем название товара для отображения на сайте
    preview = get_preview(request_id, request["category_name"])
    
    #Фильтруем пустые значения
    attributes = {k: v for k, v in attributes.items() if v}
    
    return {
        "id": request["id"],
        "category_id": request["category_id"],
        "category_name": request["category_name"],
        "created_at": request["created_at"],
        "status": request["status"],
        "generated_text": request["generated_text"],
        "preview": preview,
        "attributes": attributes
    }

#Формирование "превью" для сайта (Бренд + Модель) 
def get_preview(request_id: int, category: str):
    
    table_map = {
        'phone': 'phone_requests',
        'laptop': 'laptop_requests',
        'tv': 'tv_requests'
    }
    
    table = table_map.get(category)
    if table:
        details = execute_query(
            f"SELECT brand, model FROM {table} WHERE request_id = ?",
            (request_id,),
            fetch_one=True
        )
        if details and details["brand"] and details["model"]:
            return f"{details['brand']} {details['model']}"
    
    return f"Запрос #{request_id}"

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