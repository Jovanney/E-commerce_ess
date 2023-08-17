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
from database.models.modelos import Status, Usuario, Produto, Item
from database.shemas.schemas import UsuarioCreate, ProdutoCreate
from database.models.modelos import Pedido
from database.models.modelos import Produto
from sqlalchemy.orm import joinedload
from sqlalchemy.inspection import inspect

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

def get_user_by_email(email_user: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == email_user).first()

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

    

# Função para atualizar um produto na entidade Produto
def update_produto(db: Session, produto_id: int, new_ats: list): # Colocar o autenticação(so a loja do seu cnpj pode alterar seus produtos)
    db_produto = db.query(Produto).filter(Produto.id_produto == produto_id).first()
    if db_produto:
        atributos = ['categoria_prod', 'nome_produto', 'marca_produto', 'preco', 'especificacoes']
        for key, value in enumerate(new_ats):
            if value is not None:
                setattr(db_produto, atributos[key], value)

        db.commit()
        db.refresh(db_produto)

    return db_produto



def to_dict(obj):
    if isinstance(obj, Pedido):
        return {
            "id_pedido": obj.id_pedido,
            "preco_total": obj.preco_total,
            "itens": [to_dict(item) for item in obj.itens]
        }
    elif isinstance(obj, Item):
        return {
            "quantidade": obj.quantidade,
            "nome_produto": obj.produtos.nome_produto  # Assumindo que 'produtos' é a relação que aponta para o Produto no modelo Item
        }
    return {}

def get_pedidos_by_usuario(cpf_usuario: str, db: Session):
    pedidos = (
        db.query(Pedido)
        .options(joinedload(Pedido.itens))
        .filter(Pedido.cpf_usuario == cpf_usuario)
        .filter(Pedido.pedido_status != 1)
        .all()
    )
    
    for pedido in pedidos:
        print(f"Pedido ID: {pedido.id_pedido} - Itens: {pedido.itens}")
        
    return [to_dict(pedido) for pedido in pedidos]




# Cancelamento de Pedidos
def cancelar_pedido(pedido_id: int, cpf_usuario: str, db: Session):
    # Primeiro, verificamos se o pedido existe e pertence ao CPF fornecido
    pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id, Pedido.cpf_usuario == cpf_usuario).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.pedido_status == 1: 
        raise HTTPException(status_code=404, detail="Pedido não foi confirmado")
    
    if pedido.pedido_status == 5: # ID do status "Cancelado"
        raise HTTPException(status_code=403, detail="O pedido já foi cancelado anteriormente")

    if pedido.pedido_status == 2: # ID do status "Confirmado"
        pedido.pedido_status = 5 # Mudança para o status "Cancelado"
        db.commit()
        return {"message": "Pedido cancelado com sucesso"}
    else: # Se for o ID 3 ou ID 4, não pode ser cancelado
        raise HTTPException(status_code=403, detail="Pedido não pode mais ser cancelado")
    

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
