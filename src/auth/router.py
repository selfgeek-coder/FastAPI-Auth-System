from fastapi import APIRouter, Depends
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.schemas import UserRegister, UserLogin
from src.database import init_db, get_db_connection
from .jwt import create_access_token, verify_token

import sqlite3

ph = PasswordHasher()
router = APIRouter(tags=["Аутенфикация API"]) # роутер аутенфикации


@router.post("/api/register")
def api_register(user: UserRegister):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))

            if cursor.fetchone(): # если курсор зафетчил хотя бы 1 юзера с такой почтой
                return {"error": "Пользователь с таким email уже существует."}

            hashed_password = ph.hash(user.password)

            cursor.execute('''INSERT INTO users (name, email, password) VALUES (?, ?, ?)''', 
                           (user.login, user.email, hashed_password))

            conn.commit()

            return {"message": "Успешная регистрация."}
    
    except sqlite3.Error as e:
        return {"error": str(e)}
    
    
@router.post("/api/login")
def login(user: UserLogin):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (user.email,))

            user_data = cursor.fetchone()

            if not user_data:
                return {"error": "Пользователя с такой почтой не найден."}
            
            user_id, name, email, hashed_password = user_data

            try:
                ph.verify(hashed_password, user.password)
                
                access_token = create_access_token(
                    data={"sub": email, "user_id": user_id, "name": name}
                )

                return {
                    "message": "Успешный вход.",
                    "token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user_id,
                        "name": name,
                        "email": email
                    }
                }
                
            except VerifyMismatchError:
                return {"error": "Неверный пароль."}

    except sqlite3.Error as e:
        return {"error": str(e)}
    
@router.get("/api/me")
def get_current_user(payload: dict = Depends(verify_token)):
    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("sub"),
        "name": payload.get("name")
    }