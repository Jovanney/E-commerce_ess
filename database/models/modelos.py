from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True

class Endereco(Base):
    __tablename__ = 'endereco'
    
    cep = Column(String(8), primary_key= True)
    rua  = Column(String(50))
    numero  = Column(Integer, primary_key= True)
    complemento  = Column(String(50), primary_key= True)
    cidade  = Column(String(50))
    estado  = Column(String(50))
    cpf_usuario = Column(String(11), ForeignKey('usuario.cpf'))
    
    usuario = relationship('Usuario', back_populates='enderecos')

class Usuario(Base):
    __tablename__ = 'usuario'

    cpf = Column(String(11), primary_key=True)
    nome = Column(String(100))
    email = Column(String(50))
    senha = Column(String(50))
    admin = Column(Boolean)
    
    enderecos = relationship('Endereco', back_populates='usuario')
    telefones = relationship('Telefone', back_populates='usuario')
    pedidos = relationship('Pedido', back_populates='usuario')

class Telefone(Base):
    __tablename__ = 'telefone'
    
    cpf_usuario = Column(String(11), ForeignKey('usuario.cpf'))
    numero = Column(String, primary_key=True)
    
    usuario = relationship('Usuario', back_populates='telefones')

class Loja(Base):
    __tablename__ = 'loja'
    
    cnpj = Column(String(14), primary_key=True)
    email = Column(String(50))
    senha = Column(String(50))
    nome = Column(String(100))
    
    produtos = relationship('Produto', back_populates='loja')
    estoque = relationship('Estoque', back_populates='loja')
class Produto(Base):
    __tablename__ = 'produto'
    
    id_produto = Column(Integer, primary_key=True)
    cnpj_loja = Column(String(14), ForeignKey('loja.cnpj'))
    categoria_prod = Column(String(50))
    nome_produto = Column(String(50))
    marca_produto=Column(String(50))
    preco = Column(String(50))
    especificacoes = Column(String(100))
    
    loja = relationship('Loja', back_populates='produtos')
    itens = relationship('Item', back_populates='produtos')
    estoque = relationship('Estoque', back_populates='produtos')
    
class Estoque(Base):
    __tablename__ = 'estoque'
    
    id_estoque = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey('produto.id_produto'))
    quantidade = Column(Integer)
    
    produtos = relationship('Produto', back_populates='estoque')
    
class Pedido(Base):
     __tablename__='pedido'
     
     id_pedido=Column(Integer, primary_key=True)
     cpf_usuario = Column(String(11), ForeignKey('usuario.cpf'))
     preco_total=Column(Float)
     status_pedido=Column(String(50))
     
     usuario = relationship('Usuario', back_populates='pedidos')
     itens = relationship('Item', back_populates='pedidos') 
class Item(Base):
    __tablename__ = 'item'
    
    id_item = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey('produto.id_produto'))
    id_pedido = Column(Integer, ForeignKey('pedido.id_pedido'))
    quantidade = Column(Integer)
    
    produtos = relationship('Produto', back_populates='itens')
    pedidos = relationship('Pedido', back_populates= 'itens')
    