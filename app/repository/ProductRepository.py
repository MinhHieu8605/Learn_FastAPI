from typing import Optional, Sequence

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from Ecommerce.app.builder.ProductSearchBuilder import ProductSearchBuilder
from Ecommerce.app.models import Product, User, Category


class ProductRepository:
    LIKE_SEARCH_FIELDS = {
        "name": Product.name,
        "brand": Product.brand,
    }
    EXACT_MATCH_FIELDS = {
        "status": Product.status,
        "category_id": Product.category_id,
        "seller_id": Product.seller_id,
        "stock": Product.stock,
    }
    def __init__(self, db: AsyncSession):
        self.db = db

    #find all
    async def get_products(
        self,
        search_builder: ProductSearchBuilder,
        page: int =1,
        page_size: int = 10
    ) -> Sequence[Product]:
        conditions = []
        conditions.extend(self.query_normal(search_builder))
        conditions.extend(self.query_special(search_builder))

        stmt = select(Product)
        stmt = self.join_tables(stmt, search_builder)

        if search_builder.category_name:
            conditions.append(Category.name.ilike(f"%{search_builder.category_name}%"))
        if search_builder.seller_name:
            conditions.append(User.user_name.ilike(f"%{search_builder.seller_name}%"))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.options(
            selectinload(Product.category),
            selectinload(Product.seller)
        )

        # result = await self.db.execute(stmt)
        return await self.pagination(stmt, page, page_size)
        # return result.scalars().all()

    def join_tables(self, stmt, search_builder):
        if search_builder.category_name:
            stmt = stmt.join(Product.category)
        if search_builder.seller_name:
            stmt = stmt.join(Product.seller)
        return stmt

    def query_normal(self, search_builder: ProductSearchBuilder):
        conditions = []

        for field_name, column in self.LIKE_SEARCH_FIELDS.items():
            value = getattr(search_builder, field_name, None)
            if value is not None:
                if isinstance(value, str):
                    conditions.append(column.ilike(f"%{value}%"))

        for field, column in self.EXACT_MATCH_FIELDS.items():
            value = getattr(search_builder, field, None)
            if value is not None:
                conditions.append(column == value)
        return conditions

    def query_special(self, search_builder: ProductSearchBuilder):
        conditions = []

        if search_builder.price_from is not None:
            conditions.append(Product.price >= search_builder.price_from)
        if search_builder.price_to is not None:
            conditions.append(Product.price <= search_builder.price_to)
        if search_builder.stock_min is not None:
            conditions.append(Product.stock >= search_builder.stock_min)

        return conditions

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.category),
                selectinload(Product.seller)
            )
        )
        return result.scalar_one_or_none()

    async def pagination(self, stmt, page: int, page_size: int):
        #query data
        data_stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(data_stmt)
        items = result.scalars().all()

        #count
        count_stmt = stmt.with_only_columns(func.count(Product.id)).order_by(None)
        total = await self.db.scalar(count_stmt)
        return items, total

    async def save(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()
