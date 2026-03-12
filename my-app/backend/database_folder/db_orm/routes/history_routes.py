from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import models  
from database.db import get_db
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

#APIRouter — это способ группировать маршруты в FastAPI
router = APIRouter(prefix="/history", tags=["history"])


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
@router.get("/{request_id}", response_model=HistoryDetailResponse)
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