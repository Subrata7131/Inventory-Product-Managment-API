from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    description: Optional[str] = None
    discount: float = 0.0
    color: str = "N/A"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    discount: Optional[float] = None


class ProductResponse(ProductBase):
    id: str

    class Config:
        from_attributes = True





