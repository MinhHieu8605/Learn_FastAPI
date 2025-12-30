from typing import AsyncGenerator

from Ecommerce.app.db.session import AsyncSessionLocal


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        yield db