from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from Ecommerce.app.api.deps import get_current_user
from Ecommerce.app.core.deps import get_db
from Ecommerce.app.models import User
from Ecommerce.app.schemas.cart import CartResponse
from Ecommerce.app.schemas.cartItems import CartItemsResponse, CartItemsCreate, CartItemsUpdate
from Ecommerce.app.services.CartService import CartService

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    result = await service.get_cart_by_user_id(current_user.id)
    return result

@router.post("/", response_model=CartItemsResponse)
async def add_to_cart(
    request: CartItemsCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    result = await service.add_item_to_cart(current_user.id, request)
    return result

@router.put("/{cart_item_id}", response_model=CartItemsResponse, status_code=status.HTTP_200_OK)
async def update_cart(
        cart_item_id: int,
        request: CartItemsUpdate,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
):
    service = CartService(db)
    return await service.update_cart_item(cart_item_id, current_user.id, request)

@router.delete("/cart_item", status_code=status.HTTP_200_OK)
async def delete_cart_items(
    cart_item_ids: List[int],
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = CartService(db)
    await service.delete_cart_item(cart_item_ids, current_user.id)
    return {"message": "Cart item has been successfully deleted."}

