from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from database import router
from database.init_data import init_database

#Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Инициализация базы данных
init_database()

#Создание приложения
app = FastAPI()

#Настройка CORS
origins = [
    "http://localhost:3000",    # Адрес, где будет крутиться React (стандартный порт)
    "http://127.0.0.1:3000",
    # Сюда можно добавить адрес будущего продакшен-сервера, например:
    # "https://my-cool-app.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Разрешаем запросы только с этих адресов
    allow_credentials=True,
    allow_methods=["*"],           # Разрешаем все HTTP-методы (GET, POST, PATCH и т.д.)
    allow_headers=["*"],           # Разрешаем все заголовки
)

#Подключение роутера
app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True) 