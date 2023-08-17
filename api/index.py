from anyio import Path
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import  create_item, create_pedido_not_confirmed, get_item, get_itens_by_pedidos, get_pedidos_by_status, get_produto, get_user_by_cpf, create_user, update_quantidade_item, update_total_price
from database.get_db import get_db
from database.models.modelos import Item, Produto, Usuario
from database.shemas.schemas import  ItemBase, ProdutoBase, UsuarioBase, UsuarioCreate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/usuarios/')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db = db, usuario_cpf=usuario.cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="cpf already registered")
    return create_user(db=db, user=usuario)

@app.get('/usuarios/{usuario_id}')
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_user_by_cpf(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_usuario

#Retorna todos os itens do carrinho "pedido nao confirmado"

@app.get('/pedidos/{cpf_user}')
def get_pedido_itens_cart(cpf_user: str, db: Session = Depends(get_db)):
    id_status = 1 #significa que o pedido esta com status "nao confirmado"
    pedido = get_pedidos_by_status(status = id_status, cpf_user=cpf_user, db = db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    return get_itens_by_pedidos(pedido=pedido, db=db)

