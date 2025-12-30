from typing import List

from pydantic import BaseModel

from Ecommerce.app.schemas.cartItems import CartItemsResponse


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemsResponse]
    total_price: float
    total_items: int

    class Config:
        from_attributes = True