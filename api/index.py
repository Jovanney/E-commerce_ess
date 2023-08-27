from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Type
from database.get_db import get_db
from database.shemas.schemas import UsuarioCreate, ProdutoCreate, Token, LojaCreate
import database.crud.crud as crud
from datetime import timedelta
from database.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, create_access_token, verify_password


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
    pedidos = crud.get_pedidos_by_usuario(cpf_usuario, db)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Usuário sem pedidos")
    return pedidos

@app.get('/pedidos/{cpf_user}')
def get_pedido_itens_cart(cpf_user: str, db: Session = Depends(get_db)):
    id_status = 1 # significa que o pedido esta com status "nao confirmado"
    pedido = crud.get_pedidos_by_status(status = id_status, cpf_user=cpf_user, db = db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    return crud.get_itens_by_pedidos(pedido=pedido, db=db)

@app.get("/users/me/")
async def read_users_me(
    current_user = Depends(crud.get_current_user)
):
    return current_user

@app.get('/produtos/{produto_id}')
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud.get_produto_by_id(db = db, produto_id=produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return db_produto

@app.put('/cancelar_pedido/{cpf_usuario}/{pedido_id}')
def cancelar_pedido_route(cpf_usuario: str, pedido_id: int, db: Session = Depends(get_db)):
    return crud.cancelar_pedido(cpf_usuario=cpf_usuario, pedido_id=pedido_id, db=db)

@app.post('/usuarios/')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_cpf(db = db, usuario_cpf=usuario.cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="cpf already registered")
    return crud.create_user(db=db, user=usuario)

@app.post('/novo-item/')
def post_item_cart(id_produto: int, usuario_cpf: str, quantidade: int, db: Session = Depends(get_db)):
    produto = crud.get_produto(id_produto=id_produto, db=db)
    pedido = crud.get_pedidos_by_status(status=1, cpf_user=usuario_cpf, db=db)

    if pedido is None:
        print('entrei')
        pedido = crud.create_pedido_not_confirmed(db=db, cpf_user=usuario_cpf)

        
    item_existente = crud.get_item(id_produto=id_produto, id_pedido=pedido.id_pedido, db=db)  # Verifica se já existe um item igual

    if item_existente is not None:  # Verifica se o item já existe no carrinho
        item_existente.quantidade += quantidade
        crud.update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
        return crud.update_quantidade_item(item=item_existente, db=db)
    else:
        itens = crud.get_itens_by_pedidos(pedido = pedido, db=db)
    
        if len(itens) >= 1:
            exist_product = crud.get_produto(id_produto=itens[0].id_produto, db=db)
            if exist_product.cnpj_loja == produto.cnpj_loja:
                crud.update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
                return crud.create_item(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            else:
                return {'ERROR': 'produto inserido nao e da mesma loja que os produtos do carrinho'}
        else:
            crud.update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            return crud.create_item(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
          
@app.post('/loja/')
def create_loja(loja: LojaCreate, db: Session = Depends(get_db)):
    db_loja = crud.get_loja_by_email(db= db, email_loja= loja.cnpj)
    if db_loja:
        raise HTTPException(status_code=400, detail="Cnpj already registered")
    return crud.create_loja_c(db=db, loja=loja)


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

@app.put("/usuario/update_senha")
def update_senha(new_password: str, old_password: str, current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    if not verify_password(old_password, current_user.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Senha antiga incorreta")
    if not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nova senha não pode ser vazia")
    crud.update_user_password(db, current_user, new_password)
    return {"detail": "Senha atualizada com sucesso"}

@app.delete("/usuario/delete")
def delete(current_user = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    crud.delete_user(db, current_user)
    return {"detail": "Usuário deletado com sucesso"}

@app.post('/produtos/')
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = crud.get_produto_by_id(db = db, produto_id=produto.id_produto)
    if db_produto:
        raise HTTPException(status_code=404, detail="id already registered")
    return crud.create_prod(db=db, produto=produto)


@app.delete('/produtos/{produto_id}')
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    crud.delete_produto_by_id(db=db, produto_id=produto_id)
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
    db_produto = crud.update_produto(db, produto_id, new_ats)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_produto

@app.delete('/remove-item')
def delete_item_for_pedido(id_produto: int, usuario_cpf: str, db: Session = Depends(get_db)):
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=usuario_cpf, db=db)

    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    
    crud.delete_item(pedido=pedido, id_produto=id_produto, db=db)  # Chamar a função para deletar o item do pedido
    return None

@app.delete('/clear-carrinho')
def clear_cart(usuario_cpf: str, db: Session = Depends(get_db)):    
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=usuario_cpf, db=db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    else:
        crud.clear_cart_by_pedido(pedido = pedido, db=db) #Tira todos os itens do pedido
        db.delete(pedido)  # Exclui o pedido
        db.commit()
