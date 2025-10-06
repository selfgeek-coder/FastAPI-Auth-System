from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    login: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    login: str
    password: str
    email: EmailStr