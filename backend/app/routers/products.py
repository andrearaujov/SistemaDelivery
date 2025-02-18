from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import ItemCardapio  # Importando o modelo do banco
from app.schemas import product as product_schemas  # Importando os schemas necessários
from app.config import get_db  # Função que fornece a sessão do banco de dados

router = APIRouter()

# Criar produto
@router.post("/produtos/", response_model=product_schemas.ProductResponse)
def create_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = ItemCardapio(nome=product.nome, preco=product.preco, descricao=product.descricao, restaurante_id=product.restaurante_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Listar produtos
@router.get("/produtos/", response_model=list[product_schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(ItemCardapio).all()

# Obter produto por ID
@router.get("/produtos/{product_id}", response_model=product_schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ItemCardapio).filter(ItemCardapio.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

# Atualizar produto
@router.put("/produtos/{product_id}", response_model=product_schemas.ProductResponse)
def update_product(product_id: int, product: product_schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ItemCardapio).filter(ItemCardapio.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db_product.nome = product.nome
    db_product.preco = product.preco
    db_product.descricao = product.descricao
    db.commit()
    db.refresh(db_product)
    return db
