from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import delete_produto_by_id, get_user_by_email, create_user, get_produto_by_id, create_prod, update_produto
from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, ProdutoCreate
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
    db_user = get_user_by_email(db = db, usuario_email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=usuario)

@app.get('/usuarios/{usuario_id}')
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_user_by_email(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_usuario

# adicionar produtos
@app.post('/produtos/')
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = get_produto_by_id(db = db, produto_id=produto.id_produto)
    if db_produto:
        raise HTTPException(status_code=404, detail="id already registered")
    return create_prod(db=db, produto=produto)

# Exibir os itens cadastrados com base no ID
@app.get('/produtos/{produto_id}')
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = get_produto_by_id(db = db, produto_id=produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return db_produto

# Deletar itens cadastrados com base no ID
@app.delete('/produtos/{produto_id}')
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    delete_produto_by_id(db=db, produto_id=produto_id)
    return {"message": "Product Deleted"}

# Update em um produto com base no ID
@app.put("/update_produto/{produto_id}")
def update_produto_route(
    produto_id: int,
    new_categoria: Optional[str] = None,
    new_nome: Optional[str] = None,
    new_marca: Optional[str] = None,
    new_preco: Optional[int] = None,
    new_especificacoes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    print(new_preco)
    new_ats = [new_categoria, new_nome, new_marca, new_preco, new_especificacoes]
    db_produto = update_produto(db, produto_id, new_ats)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_produto
