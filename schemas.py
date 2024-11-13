from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserLogin(BaseModel):
    username: str
    password: str

class OrderStatus(str, Enum):
    pending = "Pending"
    preparing = "Preparing"
    completed = "Completed"
    cancelled = "Cancelled"

class OrderCreate(BaseModel):
    customer_id: int
    items: List[dict]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    items: Optional[List[dict]] = None

class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    items: List[dict]
    class Config:
        from_attributes = True