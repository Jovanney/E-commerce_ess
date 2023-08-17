from anyio import Path
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import  create_item, create_pedido_not_confirmed, get_item, get_itens_by_pedidos, get_pedidos_by_status, get_produto, get_user_by_cpf, create_user, update_quantidade_item, update_total_price
from database.get_db import get_db
from database.models.modelos import Item, Produto, Usuario
from database.shemas.schemas import  ItemBase, ProdutoBase, UsuarioBase, UsuarioCreate, Token
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

 #Adicionar itens | Verifica se existe algum pedido "Nao confirmado", se houver, adiciona um item a esse pedido, caso nao, cria um pedido e adiciona o item 

@app.post('/novo-item/')
def post_item_cart(id_produto: int, usuario_cpf: str, quantidade: int, db: Session = Depends(get_db)):
    produto = get_produto(id_produto=id_produto, db=db)
    pedido = get_pedidos_by_status(status=1, cpf_user=usuario_cpf, db=db)

    if pedido is None:
        print('entrei')
        pedido = create_pedido_not_confirmed(db=db, cpf_user=usuario_cpf)

        
    item_existente = get_item(id_produto=id_produto, id_pedido=pedido.id_pedido, db=db)  # Verifica se já existe um item igual

    if item_existente is not None:  # Verifica se o item já existe no carrinho
        item_existente.quantidade += quantidade
        update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
        return update_quantidade_item(item=item_existente, db=db)
    else:
        itens = get_itens_by_pedidos(pedido = pedido, db=db)
    
        if len(itens) >= 1:
            exist_product = get_produto(id_produto=itens[0].id_produto, db=db)
            if exist_product.cnpj_loja == produto.cnpj_loja:
                update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
                return create_item(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            else:
                return {'ERROR': 'produto inserido nao e da mesma loja que os produtos do carrinho'}
        else:
            update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            return create_item(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
          
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

@app.put("/usuario/update_senha")
def update_senha(new_password: str, old_password: str, current_user: Type = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(old_password, current_user.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Senha antiga incorreta")
    if not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nova senha não pode ser vazia")
    update_user_password(db, current_user, new_password)
    return {"detail": "Senha atualizada com sucesso"}

@app.delete("/usuario/delete")
def delete(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_user(db, current_user)
    return {"detail": "Usuário deletado com sucesso"}
