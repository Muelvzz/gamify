from pydantic import BaseModel, EmailStr

# for register endpoint
class UserCreate(BaseModel):
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

# for login endpoint
class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# for sending/retriving games
class GameCreate(BaseModel):
    name: str
    price: float
    stock: int
    description: str
    genre: str
    date: str

class GameOut(BaseModel):
    id: int
    user_id: int

    name: str
    price: float
    stock: int
    description: str
    genre: str
    date: str

    class Config:
        orm_mode = True

class UserGamesCreate(BaseModel):
    games: list[GameCreate]

class UserGamesOut(BaseModel):
    id: int
    user_id: int
    user_name: str

    games: list[GameOut]

    class Config:
        orm_mode = True