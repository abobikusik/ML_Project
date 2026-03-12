from fastapi import APIRouter, HTTPException
from database.db import execute_query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

#APIRouter — это способ группировать маршруты в FastAPI
router = APIRouter(prefix="/api/history", tags=["history"])


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
@router.get("/", response_model=List[HistoryResponse])
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

@router.get("/{request_id}", response_model=HistoryDetailResponse)
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