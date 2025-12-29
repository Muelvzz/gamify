import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(password: str) -> str: # hashes the password provided by the user
    return pwd.hash(password)

def verify_password(plain: str, hashed: str) -> bool: # verifies the hashed_password and the plain password if they are correct
    return pwd.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # this returns a jwt