from pudantic import BaseModel, SecretStr

from schemas.users import User

class User(BaseModel):
    login: str
    password: Secretstr
    
user = User(login="test_user", password=SecretStr("pass"))

user.password.get_secret_value()

class Post