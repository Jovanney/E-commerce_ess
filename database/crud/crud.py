from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from database.models.modelos import Usuario
from database.shemas.schemas import UsuarioCreate

def get_user_by_email(usuario_email: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == usuario_email).first()

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user