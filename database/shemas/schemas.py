from pydantic import BaseModel
from typing import List

class EnderecoBase(BaseModel):
    cep: str
    rua: str
    numero: int
    complemento: str
    cidade: str
    estado: str
    cpf_usuario: str

class UsuarioBase(BaseModel):
    cpf: str
    nome: str
    email: str
    senha: str
    admin: bool

class TelefoneBase(BaseModel):
    cpf_usuario: str
    numero: str

class LojaBase(BaseModel):
    cnpj: str
    email: str
    senha: str
    nome: str

class ProdutoBase(BaseModel):
    id_produto: int
    cnpj_loja: str
    categoria_prod: str
    nome_produto: str
    marca_produto:str
    preco:str
    especificacoes:str

class EstoqueBase(BaseModel):
    id_estoque:int
    id_produto:int
    quantidade:int

class ItemBase(BaseModel):
    id_item:int
    id_produto:int
    id_pedido:int
    quantidade:int

class PedidoBase(BaseModel):
    id_pedido:int
    cpf_usuario:str 
    preco_total:float 
    status_pedido:str 

class EnderecoCreate(EnderecoBase):
    pass

class UsuarioCreate(UsuarioBase):
    enderecos: List[EnderecoBase] = []
    telefones: List[TelefoneBase] = []
    pedidos: List[PedidoBase] = []

class TelefoneCreate(TelefoneBase):
    pass

class LojaCreate(LojaBase):
    produtos : List[ProdutoBase] = []
    estoque : List[EstoqueBase] = []

class ProdutoCreate(ProdutoBase):
    itens : List[ItemBase] = []

class EstoqueCreate(EstoqueBase):
    pass

class ItemCreate(ItemBase):
    pass

class PedidoCreate(PedidoBase):
    itens : List[ItemBase] = []
