from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_category_by_id(self, id: int) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(id == Category.id)
        )
        return result.scalar_one_or_none()