from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base do pedido
class PedidoBase(BaseModel):
    usuario_id: int
    restaurante_id: int
    total: float
    status: str  # Você pode converter isso para um Enum se preferir

# Para criação, usamos os mesmos campos
class PedidoCreate(PedidoBase):
    pass

# Para atualização, talvez você queira atualizar apenas alguns campos
class PedidoUpdate(BaseModel):
    total: float
    status: str

# Modelo de resposta do pedido, incluindo identificadores e datas
class PedidoResponse(PedidoBase):
    id: int
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        orm_mode = True  # ou from_attributes = True se estiver usando Pydantic V2
