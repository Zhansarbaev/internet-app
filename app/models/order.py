from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """Статусы заказа"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key = True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable = False)
    status = Column(
        SQLAlchemyEnum(OrderStatus, values_callable = lambda obj: [e.value for e in obj]),
        default = OrderStatus.PENDING,
        nullable = False
    )
    total_amount = Column(Float, default = 0.0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    
    # Связи
    customer = relationship("Customer", back_populates = "orders")
    order_items = relationship("OrderItem", back_populates = "order", cascade = "all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id = {self.id}, customer_id = {self.customer_id}, status = '{self.status}', total = {self.total_amount})>"