from fastapi import FastAPI
from json_db_lite import JSONDatabase
from utils import json_to_dict_list # наша функция, которая будет возвращать записи из JSON файла
import os # модуль, который поможет нам настроить относительные пути к JSON
from typing import Optional # позволит нам передавать значения по умолчанию в параметры пути и запросов
from .models import Post, Category, Location, PostCreate, CategoryCreate, LocationCreate

# Получаем путь к дирректории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к файлу JSON
path_to_json = os.path.join(parent_dir, 'blog.json')


small_db = JSONDatabase(file_path=path_to_json)

app = FastAPI()


@app.get("/blogs/")
def json_to_dict_list():
    return small_db.get_all_records()


@app.get("/")
def home_page():
    return {"message": "Добро пожаловать в API блогов!"}


@app.get("/blogs/post/{category_id}", response_model=list[Post])
def get_posts(category_id: int, author: Optional[int] = None, category: Optional[int] = None, location: Optional[int] = None):
    blogs = json_to_dict_list(path_to_json)
    filtered_posts = []
    for blog in blogs:
        if blog.get("model") == "blog.post" and blog.get("fields", {}).get("category") == category_id:
            filtered_posts.append(blog)
    if author is not None:
        filtered_posts = [post for post in filtered_posts if post["fields"]["author"] == author]
        
    if location is not None:
        filtered_posts = [post for post in filtered_posts if post['fields']['location'] == location]
        
    return filtered_posts



@app.get("/blogs/category/{is_published}", response_model=list[Category])
def get_categories(is_published: bool, title: Optional[str] = None):
    blogs = json_to_dict_list(path_to_json)
    filtered_categories = []
    for blog in blogs:
        if blog.get("model") == "blog.category" and blog["fields"]["is_published"] == is_published:
            filtered_categories.append(blog)
        
    if title is not None:
        filtered_categories = [category for category in filtered_categories if title.lower() in category['fields']['title'].lower()]
        
    return filtered_categories


@app.get("/blogs/location/{is_published}", response_model=list[Location])
def get_locations(is_published: bool, name: Optional[str] = None):
    blogs = json_to_dict_list(path_to_json)
    filtered_locations = []
    for blog in blogs:
        if blog.get("model") == "blog.location" and blog["fields"]["is_published"] == is_published:
            filtered_locations.append(blog)
    if name is not None:
        filtered_locations = [location for location in filtered_locations if name.lower() in location['fields']['name'].lower()]
    return filtered_locations
