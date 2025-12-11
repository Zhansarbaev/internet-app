from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.dependencies import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix = "/customers", tags = ["Customers"])

@router.get("/", response_model = List[CustomerResponse], description = "Получить список клиентов")
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model = CustomerResponse, description = "Получить клиента по ID")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(statuc_code = status.HTTP_404_NOT_FOUND, detail = "Клиент не найден")
    return customer

@router.post("/", response_model = CustomerResponse, status_code = status.HTTP_201_CREATED, description = "Создать нового клиента")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Клиент с таким email уже существует"
        )

@router.put("/{customer_id}", response_model = CustomerResponse, description = "Обновить клиенита")
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Клиент не найден")

    update_data = customer.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    try:
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Клиент с таким email уже существует"
        )

@router.delete("/{customer_id}", status_code = status.HTTP_204_NO_CONTENT, description = "Удалить клиента")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Клиент не найден")
    
    db.delete(db_customer)
    db.commit()
    return None