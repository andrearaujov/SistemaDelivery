from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import Restaurante
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.config import get_db

#Criar resutarante
router = APIRouter(prefix="/restaurants", tags =["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = db.query(Restaurante).filter(Restaurante.cnpj == restaurant.cnpj).first()
    if db_restaurant:
        raise HTTPException(status_code=400, detail= "Restaurante com esse CNPJ já cadastrado")
    
    novo_restaurant = Restaurante(
        dono_id = restaurant.dono_id,
        nome = restaurant.nome,
        cnpj = restaurant.cnpj,
        endereco = restaurant.endereco,
        telefone = restaurant.telefone
        )
    
    db.add(novo_restaurant)
    db.commit()
    db.refresh(novo_restaurant)
    
    return novo_restaurant

@router.get("/", response_model= list[RestaurantResponse])
def get_restaurants(db:Session = Depends(get_db)):
    restaurants = db.query(Restaurante).all()
    return restaurants

@router.get("/{restaurant_id}", response_model = RestaurantResponse)
def get_restaurant(restaurant_id: int , db:Session = Depends(get_db)):
    restaurant = db.query(Restaurante).filter(Restaurante.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, restaurant_update: RestaurantUpdate, db:Session = Depends(get_db)):
    restaurant = db.query(Restaurante).filter(Restaurante.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Esse restaurante não foi encontrado")
    
    if restaurant_update.nome is not None:
        restaurant.nome = restaurant_update.nome
    if restaurant_update.cnpj is not None:
        restaurant.cnpj = restaurant_update.cnpj
    if restaurant_update.endereco is not None:
        restaurant.endereco = restaurant_update.endereco
    if restaurant_update.telefone is not None:
        restaurant.telefone = restaurant_update.telefone
        
    db.commit()
    db.refresh(restaurant)
        
    return restaurant

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurante).filter(Restaurante.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    db.delete(restaurant)
    db.commit()
    return
    