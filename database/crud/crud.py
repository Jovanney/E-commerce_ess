from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from database.models.modelos import Usuario, Item
from database.shemas.schemas import UsuarioCreate
from database.models.modelos import Pedido
from database.models.modelos import Produto
from sqlalchemy.orm import joinedload
from sqlalchemy.inspection import inspect



def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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





    
