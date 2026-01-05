from decimal import Decimal
from optparse import Option
from typing import Optional

from pydantic import BaseModel


class CartItemsBase(BaseModel):
    product_id: int
    quantity: int

class CartItemsCreate(CartItemsBase):
    pass

class CartItemsUpdate(BaseModel):
    quantity: Optional[int] = None

class CartItemsResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True