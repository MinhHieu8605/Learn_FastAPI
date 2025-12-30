from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from Ecommerce.app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_ECOMMERCE_URI,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)