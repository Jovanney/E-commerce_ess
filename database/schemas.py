from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    nomecompleto: str
    email: str
    senha: str
    endereco_id: Optional[int]

class EnderecoCreate(BaseModel):
    rua: str
    numero: int
    complemento: Optional[str]
    cidade: str
    estado: str
    cep: str

class PedidoCreate(BaseModel):
    valor_total: int
    usuario_id: int
