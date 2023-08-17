from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from database.models.modelos import Status, Usuario, Produto
from database.shemas.schemas import UsuarioCreate, ProdutoCreate

def get_user_by_email(usuario_email: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == usuario_email).first()

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_produto_by_id(produto_id: int, db: SessionLocal = Depends(get_db)):
    return db.query(Produto).filter(Produto.id_produto == produto_id).first()

def create_prod(db: Session, produto: ProdutoCreate):
    db_prod = Produto(**produto.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


#Delete de colocar itens no menu principal da sua loja
def delete_produto_by_id(db: Session, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.id_produto == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_produto)
    db.commit()
