from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import Pedido
from app.schemas.order import PedidoCreate, PedidoResponse, PedidoUpdate
from app.config import get_db

# Remova o prefixo daqui
router = APIRouter(tags=["orders"])

# Criar um novo pedido
@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Pedido(
        usuario_id=order.usuario_id,
        restaurante_id=order.restaurante_id,
        total=order.total,
        status=order.status
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

# Listar todos os pedidos
@router.get("/", response_model=list[PedidoResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Pedido).all()
    return orders

# Obter um pedido por ID
@router.get("/{order_id}", response_model=PedidoResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

# Atualizar um pedido
@router.put("/{order_id}", response_model=PedidoResponse)
def update_order(order_id: int, order_update: PedidoUpdate, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    order.total = order_update.total
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return order

# Excluir um pedido
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(order)
    db.commit()
    return
