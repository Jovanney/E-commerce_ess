from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Type
from database.get_db import get_db
from database.models.modelos import Produto
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

@app.get('/pedidos')
def get_pedidos_route(db: Session = Depends(get_db), current_user: Type = Depends(crud.get_current_user)):
    pedidos = crud.get_pedidos_by_usuario(current_user.cpf,db)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Usuário sem pedidos")
    return pedidos

@app.get('/my-cart/')
def get_pedido_itens_cart(current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    id_status = 1 #significa que o pedido esta com status "nao confirmado"
    pedido = crud.get_pedidos_by_status(status = id_status, cpf_user=current_user.cpf, db = db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    retorno = crud.get_produtos_by_cart(pedido=pedido, db=db)
    return retorno

@app.get("/users/me/")
async def read_users_me(
    current_user = Depends(crud.get_current_user)
):
    return current_user

# Exibir os itens cadastrados com base no ID
@app.get('/view_Produtos/{produto_id}')
def read_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud.get_produto_by_id(db = db, produto_id=produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return db_produto

@app.put('/cancelar_pedido/{pedido_id}')
def cancelar_pedido_route(pedido_id: int, db: Session = Depends(get_db), current_user: Type = Depends(crud.get_current_user)):
    return crud.cancelar_pedido(cpf_usuario = current_user.cpf, pedido_id=pedido_id, db=db)

@app.post('/usuarios/')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_cpf(db = db, usuario_cpf=usuario.cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="cpf already registered")
    return crud.create_user(db=db, user=usuario)

@app.post('/novo-item/{id_produto}/{quantidade}')
def post_item_cart(id_produto: int, quantidade: int, current_user: Type = Depends(crud.get_current_user),  db: Session = Depends(get_db)):
    produto = crud.get_produto(id_produto=id_produto, db=db)
    pedido = crud.get_pedidos_by_status(status=1, cpf_user=current_user.cpf, db=db)
    
    if pedido is None:
        pedido = crud.create_pedido_not_confirmed(db=db, cpf_user=current_user.cpf)

        
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
                raise HTTPException(status_code=404, detail="Produto inserido nao e da mesma loja que os produtos do carrinho")
        else:
            crud.update_total_price(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            crud.create_item(db=db, produto=produto, pedido=pedido, quantidade=quantidade)
            return {
                    "id_item": pedido,
                    "id_produto": id_produto,
                    "quantidade": quantidade
                }
          
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

# adicionar produtos
@app.post('/add_produtos/')
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db), current_user: Type = Depends(crud.get_current_user)):
    # Consultar o banco de dados para encontrar o último id_produto usado
    last_product = db.query(func.max(Produto.id_produto)).scalar()
    # Incrementar o último id_produto encontrado
    new_id_produto = last_product + 1 if last_product else 1
    
    produto.id_produto = new_id_produto
    produto.cnpj_loja = current_user.cnpj
    db_produto = crud.get_produto_by_id(db=db, produto_id=new_id_produto)
    if db_produto:
        raise HTTPException(status_code=404, detail="id already registered")
    
    return crud.create_prod(db=db, produto=produto)


# Deletar produtos cadastrados com base no ID
@app.delete('/del_produtos/{produto_id}')
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    crud.delete_produto_by_id(db=db, produto_id=produto_id)
    return {"message": "Product Deleted"}

# Update em um produto com base no ID
@app.put("/update_produto/{produto_id}")
def update_produto_route(
    produto_id: int,
    categoria_prod: Optional[str] = None,
    nome_produto: Optional[str] = None,
    marca_produto: Optional[str] = None,
    preco: Optional[int] = None,
    especificacoes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    new_ats = [categoria_prod, nome_produto, marca_produto, preco, especificacoes]
    db_produto = crud.update_produto(db, produto_id, new_ats)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_produto


# Exibir todos os produtos cadastrados
@app.get('/All_Produtos/')
def read_all_produtos(db: Session = Depends(get_db)):
    produtos = crud.get_all_produtos(db=db)
    if produtos == []:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return produtos
    
    
# Exibir todos os produtos cadastrados de um cnpj especifico
@app.get('/All_Produtos_cnpj')
def read_all_produtos(db: Session = Depends(get_db), current_user: Type = Depends(crud.get_current_user)):
    produtos = crud.get_all_produtos_per_cnpj(cnpj=current_user.cnpj, db=db)
    if produtos == []:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return produtos
    
# Exibir os itens cadastrados com base no nome
@app.get('/view_Produtos_name/{nome}')
def read_produtos_por_nome(nome: str, db: Session = Depends(get_db)):
    produtos = crud.get_products_per_name(nome=nome, db=db)
    if not produtos:
        raise HTTPException(status_code=404, detail='Product not found')
    return produtos

@app.delete('/remove-item/{id_produto}')
def delete_item_for_pedido(id_produto: int, current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=current_user.cpf, db=db) 
    
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    return crud.delete_item(pedido=pedido, id_produto=id_produto, db=db) 

@app.delete('/clear-carrinho/')
def clear_cart(current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):    
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=current_user.cpf, db=db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    else:
        crud.clear_cart_by_pedido(pedido = pedido, db=db) 
        return 

@app.patch('/update-status-pedido/')
def update_status_pedido(current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=current_user.cpf, db=db)
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    else:
        new_status = crud.status_pedido_update(pedido = pedido, db=db)
        return {'new_status': new_status}
    
@app.patch('/reduce-quantity/{id_produto}')
def reduce_Quantity(id_produto: int, current_user: Type = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    pedido = crud.get_pedidos_by_status(status = 1, cpf_user=current_user.cpf, db=db)
    produto = crud.get_produto(id_produto=id_produto, db=db)
    crud.update_total_price(db=db, produto=produto, pedido=pedido, quantidade=-1)
    
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not found')
    return crud.reduce_item_quantity(pedido=pedido, id_produto=id_produto, db=db)