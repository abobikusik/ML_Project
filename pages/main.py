from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
  
app = FastAPI()

#Подключение CSS и JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main():
    return FileResponse("index.html")

#Для навигации по сайту
@app.get("/phone_form")
def get_phone_form():
    return FileResponse("phone_form.html")

@app.get("/laptop_form")
def get_laptop_form():
    return FileResponse("laptop_form.html")

@app.get("/tv_form")
def get_tv_form():
    return FileResponse("tv_form.html")

#Проверка получения данных после отправки формы
@app.post("/phone_form")
def print_phone_data(data = Body()):
    a1 = data["brand"]
    a2 = data["model"]
    a3 = data["screen_size"]
    a4 = data["display_type"]
    a5 = data["screen_refresh"]
    print(f"{a1}, {a2}, {a3}, {a4}, {a5}")

@app.post("/laptop_form")
def print_laptop_data(data = Body()):
    a1 = data["brand"]
    a2 = data["model"]
    a3 = data["screen_size"]
    a4 = data["display_type"]
    a5 = data["screen_refresh"]
    print(f"{a1}, {a2}, {a3}, {a4}, {a5}")

@app.post("/tv_form")
def print_tv_data(data = Body()):
    a1 = data["brand"]
    a2 = data["model"]
    a3 = data["screen_size"]
    a4 = data["display_type"]
    a5 = data["screen_refresh"]
    return  print(f"{a1}, {a2}, {a3}, {a4}, {a5}")