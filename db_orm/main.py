from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import uvicorn
from routes import form_routes, history_routes
from database.init_data import init_database

#Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Инициализация базы данных
init_database()

#Создание приложения
app = FastAPI()

#Подключение статческих файлов
app.mount("/static", StaticFiles(directory="views/static"), name="static")

#Подключение роутеров
app.include_router(form_routes.router)
app.include_router(history_routes.router)


@app.get("/")
def main():
    return FileResponse("views/index.html")

@app.get("/history")
def main():
    return FileResponse("views/history.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000) 