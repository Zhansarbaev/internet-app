from pydantic import BaseModel, Field
from typing import Optional

# Схемы для продукта 

class ProductBase(BaseModel): # Базовая схема продукта

    name: str = Field(..., min_length = 1, max_length = 255)
    description: Optional[str] = None
    price: float = Field(..., gt = 0)
    stock: int = Field(default = 0, ge = 0)

class ProductCreate(ProductBase):

    pass

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length = 1, max_length = 255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt = 0)
    stock: Optional[int] = Field(None, ge = 0)

class ProductResponse(ProductBase):

    id: int

    class Config:
        from_attributes = True
