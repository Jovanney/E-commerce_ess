from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import create_loja_c, get_loja_by_cnpj, get_user_by_email, create_user
from database.get_db import get_db
from database.shemas.schemas import LojaCreate, UsuarioCreate
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

@app.post('/loja/')
def create_loja(loja: LojaCreate, db: Session = Depends(get_db)):
    db_loja = get_loja_by_cnpj(db= db, cnpj_loja = loja.cnpj)
    if db_loja:
        raise HTTPException(status_code=400, detail="Cnpj already registered")
    return create_loja_c(db=db, loja=loja)

@app.get('/loja/{loja_cnpj}')
def read_loja(loja_cnpj: str, db: Session = Depends(get_db)):
    db_loja = get_loja_by_cnpj(db=db, cnpj_loja=loja_cnpj)
    if db_loja is None:
        raise HTTPException(status_code=404, detail='Loja not found')
    return db_loja

@app.get('/usuarios/{usuario_id}')
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_user_by_email(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_usuario
