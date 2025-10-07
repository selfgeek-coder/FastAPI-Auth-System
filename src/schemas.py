from pydantic import BaseModel, EmailStr, field_validator

class UserRegister(BaseModel):
    login: str
    password: str
    email: EmailStr

    @field_validator('login')
    @classmethod
    def validate_login(cls, v):
        if len(v) < 3:
            raise ValueError('Логин должен содержать минимум 3 символа.')
        
        if ' ' in v:
            raise ValueError('Логин не должен содержать пробелы.')
        
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов.')
        
        return v

class UserLogin(BaseModel):
    login: str
    password: str
    email: EmailStr

    @field_validator('login')
    @classmethod
    def validate_login(cls, v):
        if len(v) < 3:
            raise ValueError('Логин должен содержать минимум 3 символа.')
        
        if ' ' in v:
            raise ValueError('Логин не должен содержать пробелы.')
        
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        return v