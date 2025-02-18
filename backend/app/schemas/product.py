from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    nome: str
    preco: float
    descricao: Optional[str] = None
    restaurante_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  
