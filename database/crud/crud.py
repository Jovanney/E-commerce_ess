from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database.get_db import SessionLocal, get_db
from database.models.modelos import Item, Pedido, Produto, Usuario
from database.shemas.schemas import  ItemBase, ProdutoBase, UsuarioCreate
from sqlalchemy.inspection import inspect
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


def get_user_by_cpf(usuario_cpf: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.cpf == usuario_cpf).first()

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
    
def delete_user(db, user):
    db.delete(user)
    db.commit()

