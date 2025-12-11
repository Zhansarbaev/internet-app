from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix = "/orders", tags = ["Orders"])

@router.get("/", response_model = List[OrderResponse], description = "Получить список заказов")
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model = OrderResponse, description = "Получить заказ по ID")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Заказ не найден")
    return order

@router.post("/", response_model = OrderResponse, status_code = status.HTTP_201_CREATED, description = "Создать новый заказ")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Клиент не найден")
    
    # Создание заказа
    db_order = Order(customer_id = order_data.customer_id)
    db.add(db_order)
    db.flush()  # чтобы получить ID заказа до коммита

    total_amount = 0.0

    # Добавление позиций заказа
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Продукт с ID {item.product_id} не найден"
            )
        
        # Проверка наличия на складе
        if product.stock < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"Недостаточно товара '{product.name}' на складе. Доступно: {product.stock}"
            )
        
        # Создание позиции заказа
        order_item = OrderItem(
            order_id = db_order.id,
            product_id = product.id,
            quantity = item.quantity,
            price = product.price
        )

        db.add(order_item)

        # Обновление остатка
        product.stock -= item.quantity

        # Обновление  суммы заказа
        total_amount += product.price * item.quantity
    
    # Установка общей суммы
    db_order.total_amount = total_amount

    db.commit()
    db.refresh(db_order)
    return db_order

@router.patch("{order_id}", response_model = OrderResponse, description = "Обновить статус заказа")
def update_order_status(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Заказ не найден")
    
    if order_update.status is not None:
        db_order.status = order_update.status
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", status_code = status.HTTP_204_NO_CONTENT, description = "Удалить заказ")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.dbuery(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Заказ не найден")
    
    db.delete(db_order)
    db.commit()
    return None


        
