from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel): # for register endpoint
    username: str
    email: EmailStr
    password: str
    role: str = "buyer"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class Login(BaseModel): # for login endpoint
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str