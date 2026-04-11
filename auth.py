from werkzeug.security import generate_password_hash, check_password_hash
from db import users_collection

def register_user(username, password):
    existing = users_collection.find_one({"username": username})
    
    if existing:
        return False
    
    hashed_password = generate_password_hash(password)
    
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })
    
    return True


def login_user(username, password):
    user = users_collection.find_one({"username": username})
    
    if not user:
        return None
    
    if check_password_hash(user["password"], password):
        return user
    
    return None