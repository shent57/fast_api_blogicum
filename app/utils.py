from json_db_lite import JSONDatabase
import os

# Получаем путь к дирректории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к файлу JSON
path_to_json = os.path.join(parent_dir, 'blog.json')

# инициализация объекта
db = JSONDatabase(file_path=path_to_json)

# получаем все записи
def get_all_records():
    return db.get_all_records()

# добавляем пост
def add_post(post_data: dict):
    all_records = db.get_all_records()
    posts = [record for record in all_records if record.get("model") == "blog.post"]
    new_pk = max((p.get("pk", 0) for p in posts), default=0) + 1
    if 'pub_date' in post_data:
        post_data['pub_date'] = post_data['pub_date'].strftime('%Y-%m-%dT%H:%M:%S')
    
    new_post = {
        "model": "blog.post",
        "pk": new_pk,
        "fields": post_data
    }
    
    db.add_records(new_post)
    return True

# обновляем пост
def update_post(update_post: dict, new_data: dict):
    db.update_record_by_key(update_post, new_data)
    return True

# удаляем пост
def delete_post(key: str, value):
    db.delete_record_by_key(key, value)
    return True

# добавляем категорию
def add_category(category_data: dict):
    db.add_records(category_data)
    return True

# обновляем категорию
def update_category(update_category: dict, new_data: dict):
    db.update_record_by_key(update_category, new_data)
    return True

# удаляем категорию
def delete_category(key: str, value):
    db.delete_record_by_key(key, value)
    return True

# добавляем локацию
def add_location(location_data: dict):
    db.add_records(location_data)
    return True

# обновляем локацию
def update_location(update_location: dict, new_data: dict):
    db.update_record_by_key(update_location, new_data)
    return True

# удаляем локацию
def delete_location(key: str, value):
    db.delete_record_by_key(key, value)
    return True

