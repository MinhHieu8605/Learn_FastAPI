from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Ecommerce.app.models import Cart, CartItem


class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_user_id(self, user_id: int) -> Cart | None:
        result = await self.db.execute(
            select(Cart).where(Cart.user_id == user_id)
            .options(
                selectinload(Cart.cart_items)
                .selectinload(CartItem.product)
            )
        )
        return result.scalar_one_or_none()

    async def save(self, cart: Cart):
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart

