from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class OrderStatus(str, Enum):
    
    """Статусы заказов"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "cancelled"

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable = False)
    status = Column(Enum(OrderStatus), default = OrderStatus.PENDING, nullable = False)
    total_amount = Column(Float, default = 0.0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())

    # связи 
    customer = relationship('Customer', back_populates = 'orders')
    order_items = relationship('OrderItem', back_populates = 'order', cascade = 'all, delete-orphan')

    def __repr__(self):
        return f"<Order(id = {self.id}, customer_id = {self.customer_id}, status = '{self.status}', total = {self.total_amount})>"
    