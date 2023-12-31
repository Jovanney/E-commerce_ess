from datetime import timedelta, datetime
from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt

import database.crud.crud as crud 
# from database.crud.crud import get_loja_by_email, get_user_by_email
from database.get_db import SessionLocal, get_db

SECRET_KEY = "2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate(email: str, password: str, db: SessionLocal = Depends(get_db)):
    user = crud.get_user_by_email(db = db, email_user = email)
    store = crud.get_loja_by_email(db = db, email_loja= email)
    entity = user if user else store
    if not entity:
        return False
    if not verify_password(password, entity.senha):
        return False
    return entity

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt