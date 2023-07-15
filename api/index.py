from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import get_db
from database.models.modelos import Usuario, Endereco, Pedido
from database.shemas.schemas import UsuarioCreate, EnderecoCreate, PedidoCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/usuarios/')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get('/usuarios/{usuario_id}')
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail='Usuario not found')
    return db_usuario

@app.post('/enderecos/')
def create_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    db_endereco = Endereco(**endereco.dict())
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco

@app.get('/enderecos/{endereco_id}')
def read_endereco(endereco_id: int, db: Session = Depends(get_db)):
    db_endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if not db_endereco:
        raise HTTPException(status_code=404, detail='Endereco not found')
    return db_endereco

@app.post('/pedidos/')
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.get('/pedidos/{pedido_id}')
def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail='Pedido not found')
    return db_pedido
