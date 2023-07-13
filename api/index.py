from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/produtos")
def get_produtos():
    return {"message": "Hello World"}

@app.post("/cadastrarProduto")
def post_produto():
    return {"message": "produto cadastrado"} 

@app.patch("/editarProduto/{produto_id}")
def update_produto():
    return {"message": "produto atualizado"} 

@app.get("/lerPedidos")
def read_pedido():
    return {"message": "lista de pedidos"}

@app.post("/cadastrarUsuario")
def post_produto():
    return {"message": "usuário cadastrado"} 

@app.patch("/editarUsuario/{usuario_id}")
def update_produto():
    return {"message": "usuario atualizado"} 
