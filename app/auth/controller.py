from werkzeug.security import check_password_hash
from typing import Optional

mock_user= {
    "user_id":1,
    "username": "testadmin",
    "password_hash":"scrypt:32768:8:1$0XJHXabUr9zJoN8g$30f79c5dd3bc764a34c0bb7baec3e49bd741b7ef4b7a3544c506df4b6c372aa08f715fd1e3fbe6bb1fadb340ee24e5085ccd0ef786605c4491e58addccabb76a",
    "email": "admin@example.com"
}

def authenticate_user(username: str, password: str) -> Optional[int]:

    if username != mock_user["username"]:
        return None
    
    if not check_password_hash(mock_user["password_hash"], password):
        return None
    
    return mock_user["user_id"]

