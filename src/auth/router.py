from fastapi import APIRouter, Depends, HTTPException, status
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.schemas import UserRegister, UserLogin
from src.database import get_db_connection
from .jwt import create_access_token, verify_token

import sqlite3

ph = PasswordHasher()
router = APIRouter(tags=["API Аутенфикации"],
                   prefix="/api") # роутер аутенфикации

@router.post("/register")
def api_register(user: UserRegister):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))

            if cursor.fetchone(): # если курсор зафетчил хотя бы 1 юзера с такой почтой
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "USER_ALREADY_EXISTS",
                        "message": "Пользователь с такой почтой уже существует."
                    }
                )

            hashed_password = ph.hash(user.password)

            cursor.execute('''INSERT INTO users (name, email, password) VALUES (?, ?, ?)''', 
                           (user.login, user.email, hashed_password))

            conn.commit()

            return {
                "success": True,
                "message": "Успешная регистрация.",
                "data": {
                    "email": user.email,
                    "login": user.login
                }
            }
    
    except sqlite3.Error as e:
        return {"error": str(e)}
    
    
@router.post("/login")
def login(user: UserLogin):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (user.email,))

            user_data = cursor.fetchone()

            if not user_data:
                raise HTTPException(
                    status = status.HTTP_401_UNAUTHORIZED,
                    detail = {
                        "error": "USER_NOT_FOUND",
                        "message": "Пользолватель с такой почтой не найден."
                        }
                )
            
            user_id, name, email, hashed_password = user_data

            try:
                ph.verify(hashed_password, user.password)
                
                access_token = create_access_token(
                    data={"sub": email, "user_id": user_id, "name": name}
                )

                return {
                    "success": True,
                    "message": "Успешный вход.",
                    "data": {
                        "token": access_token,
                        "token_type": "bearer",
                        "user": {
                            "id": user_id,
                            "name": name,
                            "email": email
                        }
                    }
                }
                
            except VerifyMismatchError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error":"INVALID_PASSWORD",
                        "message":"Неверный логин или пароль."
                        }
                )

    except sqlite3.Error as e:
        print(str(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "DATABASE_ERROR",
                "message": "Ошибка базы данных при входе."
            }
        )
    
    
@router.get("/me")
def get_current_user(payload: dict = Depends(verify_token)):
    return {
        "uid": payload.get("user_id"),
        "email": payload.get("sub"),
        "name": payload.get("name")
    }