from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CustomerBase(BaseModel): # Базовая схема клиента

    name: str = Field(..., min_length = 1, max_length = 255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length = 20)

class CustomerCreate(CustomerBase):
    
    pass

class CustomerUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length = 1, max_length = 255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length = 20)

class CustomerResponse(CustomerBase):

    id: int

    class Config:
        from_attributes = True
