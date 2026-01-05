from typing import List, Any, Coroutine, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.models import CartItem


class CartItemsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_cart_id_and_product_id(self, cart_id: int, product_id: int):
        result = await self.db.execute(
            select(CartItem)
            .where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id

            )
        )
        return result.scalar_one_or_none()

    async def find_by_id(self, cart_item_id: int):
        return await self.db.get(CartItem, cart_item_id)

    async def find_by_ids(self, ids: List[int]) -> Sequence[CartItem]:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.id.in_(ids))
        )
        return result.scalars().all()

    async def save(self, cart_items: CartItem):
        self.db.add(cart_items)
        await self.db.commit()
        await self.db.refresh(cart_items)
        return cart_items

    async def delete(self, cart_items: CartItem) -> None:
        await self.db.delete(cart_items)