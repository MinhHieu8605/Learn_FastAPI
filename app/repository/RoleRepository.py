from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.models.Role import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_roles_by_codes(self, codes: list[str]):
        result = await self.db.execute(
            select(Role).where(Role.code.in_(codes))
        )
        return result.scalars().all()