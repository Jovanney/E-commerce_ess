from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from database.get_db import SessionLocal, get_db
from database.models.modelos import Item, Pedido, Produto, Usuario, Loja
from database.shemas.schemas import UsuarioCreate, ProdutoCreate, LojaCreate
import database.auth as auth
from typing import Annotated
from jose import JWTError, jwt


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

def get_user_by_cpf(usuario_cpf: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.cpf == usuario_cpf).first()

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
    if db.query(Loja).filter(Loja.cnpj == db_prod.cnpj_loja).first() is None:
        raise HTTPException(status_code=404, detail="cnpj not found")
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

#Delete de colocar itens no menu principal da sua loja
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

# Vai pegar todos os produtos no menu geral
def get_all_produtos(db: SessionLocal = Depends(get_db)):
    return db.query(Produto).all()

# Vai pegar todos os produtos no menu geral de um cnpj especifico
def get_all_produtos_per_cnpj(cnpj:str, db: SessionLocal = Depends(get_db)):
    return db.query(Produto).filter(Produto.cnpj_loja == cnpj).all()

def get_products_per_name(nome:str, db: SessionLocal = Depends(get_db)):
    return db.query(Produto).filter(Produto.nome_produto.ilike(f'%{nome}%')).all()

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

    if not pedidos:
        return [{"mensagem": "Não há histórico de pedidos para este usuário."}]

    resultado = []
    for pedido in pedidos:
        pedido_dict = to_dict(pedido)
        pedido_dict["id_status"] = pedido.status.id_status
        resultado.append(pedido_dict)
        
    return resultado






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
    

def create_pedido_not_confirmed(db: Session, cpf_user: str):
    db_pedido = Pedido()
    db_pedido.cpf_usuario = cpf_user
    db_pedido.pedido_status = 1
    db_pedido.preco_total = 0
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def create_item(db: Session, produto: Produto, pedido: Pedido, quantidade: int):
    db_item = Item()
    db_item.quantidade = quantidade
    db_item.produtos = produto
    db_item.pedidos = pedido
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_total_price(db: Session, produto: Produto, pedido: Pedido, quantidade: int):
    pedido.preco_total = float(pedido.preco_total) + (float(produto.preco)*quantidade)
    db.commit()


def get_produto(id_produto: int, db: SessionLocal = Depends(get_db)):
    return db.query(Produto).filter(Produto.id_produto == id_produto).first()


def get_item(id_produto: int, id_pedido: int, db: SessionLocal = Depends(get_db)):
    return db.query(Item).filter((Item.id_pedido == id_pedido) & (Item.id_produto == id_produto)).first()


def get_pedidos_by_status(status: int,cpf_user:str ,db: SessionLocal = Depends(get_db)):
    return  db.query(Pedido).filter((Pedido.pedido_status == status) & (Pedido.cpf_usuario == cpf_user)).first()

def get_itens_by_pedidos(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    return db.query(Item).filter(Item.id_pedido == pedido.id_pedido).all()

def get_produtos_by_cart(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    results = (
        db.query(Item, Produto)
        .join(Produto, Produto.id_produto == Item.id_produto)
        .filter(Item.id_pedido == pedido.id_pedido)
        .all()
    )

    # Organizando os resultados para retornar para o cliente
    items_details = []
    for item, produto in results:
        items_details.append({
            "nome_produto": produto.nome_produto,
            "preco": produto.preco,
            "quantidade": item.quantidade
        })

    return items_details

def update_quantidade_item(item: Item, db: SessionLocal = Depends(get_db)):
    db.merge(item)
    db.commit()
    db.refresh(item)
    return item

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionLocal = Depends(get_db)):
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

    user = get_user_by_email(db = db, email_user = email)
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

def get_produtos_by_cart(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    results = (
        db.query(Item, Produto)
        .join(Produto, Produto.id_produto == Item.id_produto)
        .filter(Item.id_pedido == pedido.id_pedido)
        .all()
    )

    # Organizando os resultados para retornar para o cliente
    items_details = []
    for item, produto in results:
        items_details.append({
            "id": produto.id_produto,
            "nome_produto": produto.nome_produto,
            "preco": produto.preco,
            "quantidade": item.quantidade
        })

    return items_details

def get_pedidos_by_status(status: int,cpf_user:str ,db: SessionLocal = Depends(get_db)):
    return  db.query(Pedido).filter((Pedido.pedido_status == status) & (Pedido.cpf_usuario == cpf_user)).first()

def get_itens_by_pedidos(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    return db.query(Item).filter(Item.id_pedido == pedido.id_pedido).all()

def delete_item(pedido: Pedido, id_produto: int, db: SessionLocal = Depends(get_db)):
    item = get_item(id_produto=id_produto, id_pedido=pedido.id_pedido, db=db) 
    quantidade = item.quantidade
    produto = get_produto(id_produto=id_produto, db=db)
    pedido.preco_total = float(pedido.preco_total) + (float(produto.preco)*-quantidade)
    if item:
        db.delete(item)  
        db.commit()       
    else:
        raise HTTPException(status_code=404, detail="Item not found in the cart")

    return {"id": item.id_produto}
    
def clear_cart_by_pedido(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    db.delete(pedido)  
    db.commit()
    
def status_pedido_update(pedido: Pedido, db: SessionLocal = Depends(get_db)):
    new_status = 2
    pedido.pedido_status = new_status
    db.merge(pedido)
    db.commit()
    return new_status

def reduce_item_quantity(pedido: Pedido, id_produto: int, db: SessionLocal = Depends(get_db)):
    item = get_item(id_produto=id_produto, id_pedido=pedido.id_pedido, db=db) 
    quantidade = item.quantidade
    
    if item:
        item.quantidade = quantidade-1
        db.merge(item)
        db.commit()
        return {"id": item.id_produto, "quantidade": item.quantidade}
    
    else:
        raise HTTPException(status_code=404, detail="Item not found in the cart")
    