from fastapi import Depends
from passlib.context import CryptContext

from database.crud.crud import get_user_by_email
from database.get_db import SessionLocal, get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: SessionLocal = Depends(get_db)):
    user = get_user_by_email(db = db, usuario_email = username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user