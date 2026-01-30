from pydantic import BaseModel
from typing import Optional


# ১. প্রোডাক্টের সাধারণ তথ্য
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    description: Optional[str] = None


# ২. নতুন প্রোডাক্ট তৈরি করার সময় এটি লাগবে
class ProductCreate(ProductBase):
    pass


# ৩. এটিই আপনার ফাইলে মিসিং ছিল (প্রোডাক্ট আপডেট করার জন্য)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None


# ৪. ডাটাবেস থেকে তথ্য দেখানোর জন্য
class ProductResponse(ProductBase):
    id: str

    class Config:
        from_attributes = True
