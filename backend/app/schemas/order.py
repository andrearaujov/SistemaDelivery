from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base do pedido
class PedidoBase(BaseModel):
    usuario_id: int
    restaurante_id: int
    total: float
    status: str  # Você pode refatorar para usar um Enum posteriormente

# Para criação de um pedido
class PedidoCreate(PedidoBase):
    pass

# Para atualização do pedido
class PedidoUpdate(BaseModel):
    total: float
    status: str

# Modelo de resposta do pedido, incluindo os identificadores e datas
class PedidoResponse(PedidoBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        orm_mode = True  # Se estiver usando Pydantic V2, use: from_attributes = True
