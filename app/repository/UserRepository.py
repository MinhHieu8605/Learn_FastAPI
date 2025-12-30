from typing import Optional,Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from Ecommerce.app.builder.UserSearchBuilder import UserSearchBuilder
from Ecommerce.app.models import Role
from Ecommerce.app.models.User import User
from sqlalchemy.orm import selectinload

from Ecommerce.app.models.UserRole import UserRole


class UserRepository:
    USER_COLUMN_MAPPING = {
        "user_name": User.user_name,
        "full_name": User.full_name,
        "phone_number": User.phone_number,
        "email": User.email,
        "status": User.status,
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    #findAll
    async def get_users(self, search_builder: UserSearchBuilder) -> Sequence[User]:
        conditions = self.query_normal(search_builder)

        stmt = select(User).options(
            selectinload(User.user_roles).selectinload(UserRole.role)
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    def query_normal(self, search_builder: UserSearchBuilder):
        conditions = []

        for field_name, column in self.USER_COLUMN_MAPPING.items():
            value = getattr(search_builder, field_name, None)
            if value is not None:
                if isinstance(value, str):
                    conditions.append(column.ilike(f"%{value}%"))
                else:
                    conditions.append(column == value)

        if search_builder.roles:
            conditions.append(
                User.user_roles.any(
                    UserRole.role.has(Role.code.in_(search_builder.roles))
                )
            )

        return conditions
    #end find all

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
        )
        return result.scalar_one_or_none()

    async def get_user_by_user_name(self, user_name: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.user_name == user_name)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
        )
        return result.scalar_one_or_none()

    async def exists_by_user_name(self, user_name: str) -> bool:
        result = await self.db.execute(select(User).where(User.user_name == user_name))
        return result.first() is not None

    async def save(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()