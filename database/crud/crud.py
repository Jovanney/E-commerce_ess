from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database.auth as auth
from database.get_db import SessionLocal, get_db
from database.models.modelos import Loja, Usuario
from database.shemas.schemas import LojaCreate, UsuarioCreate
from jose import JWTError, jwt
from database.shemas.schemas import Token

SECRET_KEY = "2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user_by_email(usuario_email: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == usuario_email).first()

def get_loja_by_email(email_loja: str, db: SessionLocal = Depends(get_db)):
    return db.query(Loja).filter(Loja.email == email_loja).first()

def create_loja_c(db: Session, loja: LojaCreate):
    db_loja = Loja(**loja.dict())
    db_loja.senha = auth.get_password_hash(db_loja.senha)
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja)
    return db_loja

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db_user.senha = auth.get_password_hash(db_user.senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db = db, usuario_email = email)
    store = get_loja_by_email(db = db, email_loja= email)
    entity = user if user else store
    if entity is None:
        raise credentials_exception
    return entity

def update_user_password(db, user, new_password):
    hashed_password = auth.get_password_hash(new_password)
    user.senha = hashed_password
    db.merge(user)
    db.commit()