from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if db.query(models.Users).filter(models.Users.email == user.email).first(): # checks if the user already exist
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password) # hashes the password instead of plainly saving it into the database
    db_user = models.Users(username=user.username, email=user.email, password=hashed, role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.Login, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == payload.email).first() # checks if the user's email already exist

    if not user or not verify_password(payload.password, user.password): # checks if there is no existing user email or password doesn't match
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }