from sqlalchemy import Column, Integer, String, Float, Text, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), nullable = False)
    description = Column(Text, nullable = True)
    price = Column(Float, nullable = False)
    stock = Column(Integer, default = 0)

    __table_args__ = (
        CheckConstraint("price > 0", name = "check_price_positive"),
        CheckConstraint("stock >= 0", name = 'check_stock_non_negative'),
    )

    # связь с order_item (один продукт во многизх заказах)
    order_items = relationship('OrderItem', back_populates = 'product')

    def __repr__(self): #представление 
        return f"<Product(id = {self.id}, name = '{self.name}', price = {self.price})>"