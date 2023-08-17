from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import create_user, get_pedidos_by_usuario, cancelar_pedido
from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, PedidoBase
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

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
    return {"Hello": "World111"}

@app.get('/pedidos/{cpf_usuario}/')
def get_pedidos_route(cpf_usuario: str, db: Session = Depends(get_db)):
    pedidos = get_pedidos_by_usuario(cpf_usuario, db)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Usuário sem pedidos")
    return pedidos

@app.put('/cancelar_pedido/{cpf_usuario}/{pedido_id}')
def cancelar_pedido_route(cpf_usuario: str, pedido_id: int, db: Session = Depends(get_db)):
    return cancelar_pedido(cpf_usuario=cpf_usuario, pedido_id=pedido_id, db=db)



