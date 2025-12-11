from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base): # таблица связывает ордер и продукт (М:М)

    __tablename__ = 'order_items'

    id = Column(Integer, primary_key = True, index = True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable = False)
    quantity = Column(Integer, nullable = False, default = 1)
    price = Column(Float, nullable = False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name = 'check_quantity_positive'),
        CheckConstraint('price >= 0', name = 'check_price_non_negative'),
    )

    order = relationship('Order', back_populates = 'order_items')
    product = relationship('Product', back_populates = 'order_items')

    def __repr__(self):
        return f"<OrderItem(order_id = {self.order_id}, product_id = {self.product_id}, qty = {self.quantity})>"
    