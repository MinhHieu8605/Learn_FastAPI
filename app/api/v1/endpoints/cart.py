from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.api.deps import get_current_user
from Ecommerce.app.core.deps import get_db
from Ecommerce.app.models import User
from Ecommerce.app.schemas.cartItems import CartItemsResponse, CartItemsCreate
from Ecommerce.app.services.CartService import CartService

router = APIRouter()

@router.post("/", response_model=CartItemsResponse)
async def add_to_cart(
    request: CartItemsCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    result = await service.add_item_to_cart(current_user.id, request)
    return result