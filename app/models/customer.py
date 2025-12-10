from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255), nullable = False)
    email = Column(String(255), unique = True, nullable = False, index = True)
    phone = Column(String(20), nullable = True)

    # связь с заказами (1:М)
    orders = relationship('Order', back_populates = 'customer')

    def __repr__(self):
        return f"<Customer(id = {self.id}, name = '{self.name}', email = '{self.email}')>"
    
