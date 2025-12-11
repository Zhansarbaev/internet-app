from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix = '/products', tags = ['Products'])

@router.get("/", response_model = List[ProductResponse], description = "Получить список продуктов")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model = ProductResponse, description = "Получить продукт по ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product.id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Продукт не найден")
    return product

@router.post("/", response_model = ProductResponse, status_code = status.HTTP_201_CREATED, description = "Создать новый продукт")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model = ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), description = "Обновить продукт"):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Продукт не найден")
    
    update_data = product.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/product_id", status_code = status.HTTP_204_NO_CONTENT, description = "Удалить продукт")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Продукт не найден")
    
    db.delete(db_product)
    db.commit()
    return None