from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True
    pass

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nomecompleto = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    endereco_id = Column(Integer, ForeignKey('enderecos.id'))
    endereco = relationship('Endereco', back_populates='usuarios')
    pedidos = relationship('Pedido', back_populates='usuario')

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String, nullable=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    usuarios = relationship('Usuario', back_populates='endereco')

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    data_pedido = Column(DateTime, nullable=False)
    valor_total = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='pedidos')
