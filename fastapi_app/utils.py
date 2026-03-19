from json_db_lite import JSONDatabase # позволяет превратить JSON в некое подобие мини-БД.
import os # модуль, который поможет нам настроить относительные пути к JSON
from datetime import datetime

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
    if 'created_at' in post_data:
        post_data['created_at'] = post_data['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
    
    new_post = {
        "model": "blog.post",
        "pk": new_pk,
        "fields": post_data
    }
    
    db.add_records(new_post)
    return True

# обновляем пост
def update_post(update_post: dict, new_data: dict):
    if "fields" in new_data:
        fields = new_data["fields"]
        fields["pub_date"] = fields["pub_date"].strftime('%Y-%m-%dT%H:%M:%S')
        fields["created_at"] = fields["created_at"].strftime('%Y-%m-%dT%H:%M:%S')
        new_data["fields"] = fields
    db.update_record_by_key(update_post, new_data)
    return True

# удаляем пост
def delete_post(key: str, value):
    db.delete_record_by_key(key, value)
    return True

# добавляем категорию
def add_category(category_data: dict):
    all_records = db.get_all_records()
    categories = [record for record in all_records if record.get("model") == "blog.category"]
    new_pk = max((c.get("pk", 0) for c in categories), default=0) + 1
    
    if 'created_at' in category_data:
        category_data['created_at'] = category_data['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
        
    new_category = {
        "model": "blog.category",
        "pk": new_pk,
        "fields": category_data
    }
    db.add_records(new_category)
    return True

# обновляем категорию
def update_category(update_filter: dict, new_data: dict):
    if "fields" in new_data:
        fields = new_data["fields"]
        if "created_at" in fields and isinstance(fields["created_at"], datetime):
            fields["created_at"] = fields["created_at"].strftime('%Y-%m-%dT%H:%M:%S')
        new_data["fields"] = fields
    db.update_record_by_key(update_filter, new_data)
    return True

# удаляем категорию
def delete_category(key: str, value):
    db.delete_record_by_key(key, value)
    return True

# добавляем локацию
def add_location(location_data: dict):
    all_records = db.get_all_records()
    locations = [record for record in all_records if record.get("model") == "blog.location"]
    new_pk = max((l.get("pk", 0) for l in locations), default=0) + 1
    
    if 'created_at' in location_data:
        location_data['created_at'] = location_data['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
        
    new_location = {
        "model": "blog.location",
        "pk": new_pk,
        "fields": location_data
    }
    db.add_records(new_location)
    return True

# обновляем локацию
def update_location(update_filter: dict, new_data: dict):
    print(f"🔍 update_filter: {update_filter}")
    print(f"🔍 new_data: {new_data}")
    print(f"🔍 type of created_at: {type(new_data.get('fields', {}).get('created_at'))}")
    if "fields" in new_data:
        fields = new_data["fields"]
        if "created_at" in fields and not isinstance(fields["created_at"], str):
            fields["created_at"] = fields["created_at"].strftime('%Y-%m-%dT%H:%M:%S')
        new_data["fields"] = fields
    db.update_record_by_key(update_filter, new_data)
    return True

# удаляем локацию
def delete_location(key: str, value):
    db.delete_record_by_key(key, value)
    return True

