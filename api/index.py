from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.crud.crud import create_user, get_pedidos_by_usuario, cancelar_pedido
from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, PedidoBase
from database.crud.crud import delete_produto_by_id, get_user_by_email, create_user, get_produto_by_id, create_prod, update_produto
from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, ProdutoCreate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database.crud.crud import  create_item, create_pedido_not_confirmed, get_item, get_itens_by_pedidos,  get_pedidos_by_status, get_produto, get_user_by_cpf, create_user, update_quantidade_item, update_total_price, create_loja_c, delete_user, get_current_user, get_user_by_email, create_user, update_user_password

from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, Token
from datetime import timedelta
from typing import Annotated, Type
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, create_access_token, verify_password

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

@app.get('/pedidos/{cpf_usuario}/')
def get_pedidos_route(cpf_usuario: str, db: Session = Depends(get_db)):
    pedidos = get_pedidos_by_usuario(cpf_usuario, db)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Usuário sem pedidos")
    return pedidos

@app.put('/cancelar_pedido/{cpf_usuario}/{pedido_id}')
def cancelar_pedido_route(cpf_usuario: str, pedido_id: int, db: Session = Depends(get_db)):
    return cancelar_pedido(cpf_usuario=cpf_usuario, pedido_id=pedido_id, db=db)

@app.post('/usuarios/')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db = db, usuario_cpf=usuario.cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="cpf already registered")
    return create_user(db=db, user=usuario)


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
