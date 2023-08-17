from database.shemas.schemas import Token, UsuarioBase
from datetime import timedelta
from typing import Annotated, Type
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, create_access_token, verify_password
from database.crud.crud import create_loja_c, delete_user, get_current_user, get_loja_by_email, get_user_by_email, create_user, update_user_password
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
    db_loja = get_loja_by_email(db= db, email_loja= loja.cnpj)
    if db_loja:
        raise HTTPException(status_code=400, detail="Cnpj already registered")
    return create_loja_c(db=db, loja=loja)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    entity = authenticate(db = db, email = form_data.username, password = form_data.password)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": entity.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(
    current_user = Depends(get_current_user)
):
    return current_user
