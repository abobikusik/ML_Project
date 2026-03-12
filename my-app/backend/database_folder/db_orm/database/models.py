from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class Status(Base):
    #ТАБЛИЦА СТАТУСОВ ЗАПРОСОВ
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)  #'pending', 'completed', 'error'

    #Связязь с таблицей запросов
    requests = relationship("Request", back_populates="status_rel")


class Category(Base):
    #ТАБЛИЦА КАТЕГОРИЙ ТОВАРОВ
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)  #'phone', 'laptop', 'tv'

    #Связязь с таблицей запросов
    requests = relationship("Request", back_populates="category_rel")


class Request(Base):
    """Основная таблица запросов"""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    generated_text = Column(Text, nullable=True)

    # Связи со всеми таблицами 
    category_rel = relationship("Category", back_populates="requests")
    status_rel = relationship("Status", back_populates="requests")
    phone_details = relationship("PhoneRequest", back_populates="request", uselist=False, cascade="all, delete-orphan")
    laptop_details = relationship("LaptopRequest", back_populates="request", uselist=False, cascade="all, delete-orphan")
    tv_details = relationship("TvRequest", back_populates="request", uselist=False, cascade="all, delete-orphan")


class PhoneRequest(Base):
    #ТАБЛИЦА С ДЕТАЛЯМИ ТЕЛЕФОНОВ
    __tablename__ = "phone_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    #Основные характеристики телефона
    brand = Column(String)
    model = Column(String)
    screen_size = Column(String)
    display_type = Column(String)
    screen_refresh = Column(String)
    processor = Column(String)
    os = Column(String)
    cellular = Column(String)
    storage = Column(String)
    camera = Column(String)
    battery = Column(String)
    charging_speed = Column(String)
    material = Column(String)
    weight = Column(String)

    #Связь с основной таблицей запросов
    request = relationship("Request", back_populates="phone_details")


class LaptopRequest(Base):
    #ТАБЛИЦА С ДЕТАЛЯМИ НОУТБУКОВ
    __tablename__ = "laptop_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    #Основные характеристики ноутбука
    brand = Column(String)
    model = Column(String)
    screen_size = Column(String)
    display_type = Column(String)
    screen_refresh = Column(String)
    screen_resolution = Column(String)
    processor = Column(String)
    os = Column(String)
    ram = Column(String)
    ssd = Column(String)
    graphics_card = Column(String)
    vram = Column(String)
    battery = Column(String)
    power_adapter = Column(String)
    material = Column(String)
    weight = Column(String)

    #Связь с основной таблицей запросов
    request = relationship("Request", back_populates="laptop_details")


class TvRequest(Base):
    #ТАБЛИЦА С ДЕТАЛЯМИ ТЕЛЕВИЗОРОВ
    __tablename__ = "tv_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    #Основные характеристики телевизора
    brand = Column(String)
    model = Column(String)
    screen_size = Column(String)
    display_type = Column(String)
    screen_refresh = Column(String)
    screen_resolution = Column(String)
    processor = Column(String)
    audio_power = Column(String)
    speakers_channels = Column(String)
    hdmi_count = Column(String)
    hdmi_version = Column(String)
    installation = Column(String)
    material = Column(String)
    weight = Column(String)

    #Связь с основной таблицей запросов
    request = relationship("Request", back_populates="tv_details")