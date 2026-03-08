from fastapi import FastAPI, HTTPException
from json_db_lite import JSONDatabase
from .utils import get_all_records, add_post, add_location, add_category, update_post, update_category, update_location, delete_post, delete_category, delete_location
import os # модуль, который поможет нам настроить относительные пути к JSON
from typing import Optional # позволит нам передавать значения по умолчанию в параметры пути и запросов
from .models import Post, Category, Location, PostCreate, CategoryCreate, LocationCreate, CategoryUpdateFilter, CategoryUpdateData, LocationUpdateFilter, LocationUpdateData, DeleteFilter, PostUpdateFilter, PostUpdateData

# Получаем путь к дирректории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к файлу JSON
path_to_json = os.path.join(parent_dir, 'blog.json')

# инициализация объекта
small_db = JSONDatabase(file_path=path_to_json)

# Создаём приложение
app = FastAPI()

# Возврат текста на главную страницу
@app.get("/")
def home_page():
    return {"message": "Добро пожаловать в API блогов!"}

# Возвращает список всех блогов
@app.get("/blogs")
def get_blogs():
    return get_all_records()

# Данные, которые должен получить пользователь
@app.get("/blogs/post/{category_id}", response_model=list[Post]) # передаём нашу модель
def get_posts(category_id: int, author: Optional[int] = None, category: Optional[int] = None, location: Optional[int] = None):
    records = get_all_records()
    filtered_posts = []
    for record in records:
        if record.get("model") == "blog.post" and record.get("fields", {}).get("category") == category_id:
            fields = record["fields"]
            post_data = {
                "pk": record["pk"],
                "title": fields["title"],
                "text": fields["text"],
                "pub_date": fields["pub_date"],
                "is_published": fields.get("is_published", True),
                "image": fields.get("image"),
                "author": fields["author"],
                "category": fields["category"],
                "location": fields.get("location"),
                "created_at": fields["created_at"],
                "comments": []
                
            }
            filtered_posts.append(post_data)
    if author is not None:
        filtered_posts = [post for post in filtered_posts if post["author"] == author]
        
    if location is not None:
        filtered_posts = [post for post in filtered_posts if post['location'] == location]
        
    return filtered_posts


@app.post("/blogs/post")
def create_post(post: PostCreate):
    post_dict = post.dict()
    if add_post(post_dict):
        return {"message": "Пост успешно добавлен!"}
    else:
        return {"message": "Ошибка при добавлении поста"}
    

@app.put("/blogs/post")
def update_post_handler(filter_post: PostUpdateFilter, new_data: PostUpdateData):
    check = update_post({"pk": filter_post.post_id}, {"fields": new_data.dict()})
    if check:
        return {"message": "Пост успешно обновлен!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении поста" )
    

@app.delete("/blogs/post")
def delete_post_handler(delete_filter: DeleteFilter):
    check = delete_post(delete_filter.key, delete_filter.value)
    if check:
        return {"message": "Пост успешно удален!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении поста" )


@app.get("/blogs/category/{is_published}", response_model=list[Category])
def get_categories(is_published: bool, title: Optional[str] = None):
    blogs = get_all_records()
    filtered_categories = []
    for blog in blogs:
        if blog.get("model") != "blog.category":
            continue
        
        fields = blog.get("fields", {})
        
        required_fields = ["title", "description", "slug", "created_at"]
        if not all(field in fields for field in required_fields):
            continue
        
        if fields["is_published"] == is_published:
            category_data = {
                "model": blog["model"],
                "pk": blog["pk"],
                "fields": fields
            }
            filtered_categories.append(category_data)
            
    if title is not None:
        filtered_categories = [category for category in filtered_categories if title.lower() in category['fields']['title'].lower()]
        
    return filtered_categories


@app.post("/blogs/category")
def create_category(category: CategoryCreate):
    category_dict = category.dict()
    if add_category(category_dict):
        return {"message": "Категория успешно добавлена!"}
    else:
        return {"message": "Ошибка при добавлении категории"}


@app.put("/blogs/category")
def update_category_handler(filter_category: CategoryUpdateFilter, new_data: CategoryUpdateData):
    check = update_category({"pk": filter_category.category_id}, {"fields": new_data.dict()})
    if check:
        return {"message": "Категория успешно обновлена!"}
    else:        
        raise HTTPException(status_code=400, detail="Ошибка при обновлении категории" )


@app.delete("/blogs/category")
def delete_category_handler(delete_filter: DeleteFilter):
    check = delete_category(delete_filter.key, delete_filter.value)
    if check:
        return {"message": "Категория успешно удалена!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении категории" )
    

@app.get("/blogs/location/{is_published}", response_model=list[Location])
def get_locations(is_published: bool, name: Optional[str] = None):
    blogs = get_all_records()
    filtered_locations = []
    for blog in blogs:
        if blog.get("model") != "blog.location":
            continue
        
        fields = blog.get("fields", {})
        
        if "name" not in fields or "created_at" not in fields:
            continue
        
        if fields.get("is_published") == is_published:
            location_data = {
                "model": blog["model"],
                "pk": blog["pk"],
                "fields": fields
            }
            filtered_locations.append(location_data)
            
    if name is not None:
        filtered_locations = [location for location in filtered_locations if name.lower() in location['fields']['name'].lower()]
    return filtered_locations


@app.post("/blogs/location")
def create_location(location: LocationCreate):
    location_dict = location.dict()
    if add_location(location_dict):
        return {"message": "Местоположение успешно добавлено!"}
    else:
        return {"message": "Ошибка при добавлении местоположения"}
    
    
    
@app.put("/blogs/location")
def update_location_handler(filter_location: LocationUpdateFilter, new_data: LocationUpdateData):
    check = update_location({"pk": filter_location.location_id}, new_data.dict()
                            )
    if check:
        return {"message": "Местоположение успешно обновлено!"}
    else:        
        raise HTTPException(status_code=400, detail="Ошибка при обновлении местоположения" )
    
    
@app.delete("/blogs/location")
def delete_location_handler(delete_filter: DeleteFilter):
    check = delete_location(delete_filter.key, delete_filter.value)
    if check:
        return {"message": "Местоположение успешно удалено!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении местоположения" )