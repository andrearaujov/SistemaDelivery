from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum, func
from sqlalchemy.orm import relationship
from app.config import Base
import enum

# Enum para diferenciar consumidor e restaurante
class TipoUsuario(enum.Enum):
    consumidor = "consumidor"
    restaurante = "restaurante"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(50))
    endereco = Column(String(255))
    tipo = Column(Enum(TipoUsuario), nullable=False, default=TipoUsuario.consumidor)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="usuario")
    avaliacoes = relationship("Avaliacao", back_populates="usuario")
    restaurante = relationship("Restaurante", back_populates="dono", uselist=False)

class Restaurante(Base):
    __tablename__ = "restaurantes"
    
    id = Column(Integer, primary_key=True, index=True)
    dono_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=False)
    endereco = Column(String(255), nullable=False)
    telefone = Column(String(50))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    dono = relationship("Usuario", back_populates="restaurante")
    cardapio = relationship("ItemCardapio", back_populates="restaurante")
    pedidos = relationship("Pedido", back_populates="restaurante")
    avaliacoes = relationship("Avaliacao", back_populates="restaurante")

class ItemCardapio(Base):
    __tablename__ = "itens_cardapio"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    preco = Column(Float, nullable=False)
    imagem_url = Column(String(255))
    categoria = Column(String(100))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    restaurante = relationship("Restaurante", back_populates="cardapio")
    itens_pedido = relationship("ItemPedido", back_populates="item_cardapio")

# Enum para status dos pedidos
class StatusPedido(enum.Enum):
    pendente = "pendente"
    confirmado = "confirmado"
    preparando = "preparando"
    a_caminho = "a_caminho"
    entregue = "entregue"
    cancelado = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(Enum(StatusPedido), nullable=False, default=StatusPedido.pendente)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos")
    restaurante = relationship("Restaurante", back_populates="pedidos")
    itens_pedido = relationship("ItemPedido", back_populates="pedido")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    item_cardapio_id = Column(Integer, ForeignKey("itens_cardapio.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco = Column(Float, nullable=False)
    
    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens_pedido")
    item_cardapio = relationship("ItemCardapio", back_populates="itens_pedido")

# Enum para status de pagamento
class StatusPagamento(enum.Enum):
    pendente = "pendente"
    concluido = "concluido"
    falhou = "falhou"

class Pagamento(Base):
    __tablename__ = "pagamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    valor = Column(Float, nullable=False)
    metodo_pagamento = Column(String(50))  # Exemplo: cartão de crédito, boleto, pix
    status = Column(Enum(StatusPagamento), nullable=False, default=StatusPagamento.pendente)
    transacao_id = Column(String(255))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    pedido = relationship("Pedido", back_populates="pagamento")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"), nullable=False)
    nota = Column(Integer, nullable=False)  # Nota de 1 a 5
    comentario = Column(Text)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="avaliacoes")
    restaurante = relationship("Restaurante", back_populates="avaliacoes")
