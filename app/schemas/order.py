from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):

    product_id: int
    quantity: int = Field(..., gt = 0)

class OrderItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderBase(BaseModel):

    customer_id: int
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(BaseModel):

    customer_id: int
    items: List[OrderItemCreate] = Field(..., min_length = 1)

class OrderUpdate(BaseModel):

    status: Optional[OrderStatus] = None

class OrderResponse(BaseModel):

    id: int
    customer_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True