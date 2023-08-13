from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from database.models.modelos import Loja, Usuario
from database.shemas.schemas import LojaCreate, UsuarioCreate

def get_user_by_email(usuario_email: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == usuario_email).first()

def get_loja_by_cnpj(cnpj_loja: str, db: SessionLocal = Depends(get_db)):
    return db.query(Loja).filter(Loja.cnpj == cnpj_loja).first()

def create_loja_c(db: Session, loja: LojaCreate):
    db_loja = Loja(**loja.dict())
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja)
    return db_loja

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user