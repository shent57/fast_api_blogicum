from fastapi import FastAPI
from utils import json_to_dict_list # наша функция, которая будет возвращать записи из JSON файла
import os # модуль, который поможет нам настроить относительные пути к JSON
from typing import Optional # позволит нам передавать значения по умолчанию в параметры пути и запросов


# Получаем путь к дирректории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к файлу JSON
path_to_json = os.path.join(parent_dir, 'fastapi_data.json')


app = FastAPI()


@app.get("/notes/") # Обозначает, что эта функция будет обрабатывать GET запросы по пути /notes/
def get_all_notes(): # Когда клиент отправляет GET запрос на /notes/, эта функция будет вызвана
    return json_to_dict_list(path_to_json) # Возвращаем все заметки

@app.get("/")
def home_page():
    return {"message": "Добро пожаловать в API заметок!"}