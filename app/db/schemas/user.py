# app/db/schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class UserCreate(UserBase):
    # Remove the password field if not needed
    pass

class UserUpdate(UserBase):
    # You can add fields needed for updating users
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str