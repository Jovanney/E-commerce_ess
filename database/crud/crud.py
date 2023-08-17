from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database.get_db import SessionLocal, get_db
from database.models.modelos import Item, Pedido, Produto, Usuario
from database.shemas.schemas import  ItemBase, ProdutoBase, UsuarioCreate
from sqlalchemy.inspection import inspect

def get_user_by_cpf(usuario_cpf: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.cpf == usuario_cpf).first()

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#ITI
def create_pedido_not_confirmed(db: Session, cpf_user: str):
    db_pedido = Pedido()
    db_pedido.cpf_usuario = cpf_user
    db_pedido.pedido_status = 1
    db_pedido.preco_total = 0
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

#ITI
def create_item(db: Session, produto: Produto, pedido: Pedido, quantidade: int):
    db_item = Item()
    db_item.quantidade = quantidade
    db_item.produtos = produto
    db_item.pedidos = pedido
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#DODO
def update_total_price(db: Session, produto: Produto, pedido: Pedido, quantidade: int):
    pedido.preco_total = float(pedido.preco_total) + (float(produto.preco)*quantidade)
    db.commit()

#ITI
def get_produto(id_produto: int, db: SessionLocal = Depends(get_db)):
    return db.query(Produto).filter(Produto.id_produto == id_produto).first()

#ITI 
def get_item(id_produto: int, id_pedido: int, db: SessionLocal = Depends(get_db)):
    return db.query(Item).filter((Item.id_pedido == id_pedido) & (Item.id_produto == id_produto)).first()

#Dodo
def get_pedidos_by_status(status: int,cpf_user:str ,db: SessionLocal = Depends(get_db)):
    return  db.query(Pedido).filter((Pedido.pedido_status == status) & (Pedido.cpf_usuario == cpf_user)).first()
#Dodo
def get_itens_by_pedidos(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    return db.query(Item).filter(Item.id_pedido == pedido.id_pedido).all()

#ITI
def update_quantidade_item(item: Item, db: SessionLocal = Depends(get_db)):
    db.merge(item)
    db.commit()
    db.refresh(item)
    return item
