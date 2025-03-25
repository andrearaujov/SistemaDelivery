from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class RestaurantBase(BaseModel):
    nome = str
    cnpj = str
    endereco = str
    telefone = str
    
class RestaurantCreate(RestaurantBase):
    dono_id = int
    
class RestaurantUpdate(BaseModel):
    nome = Optional[str] = None
    cnpj = Optional[str]= None
    endereco = Optional[str] = None
    telefone = Optional [str] = None
    
class RestaurantResponse(RestaurantBase):
    id: int
    dono_id: int
    criado_em: datetime
    
class Config:
    orm_mode = True
    
    
