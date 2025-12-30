import math
from typing import Optional, List

from Ecommerce.app.converter.ProductConverter import to_product_response, create_product_to_entity, \
    update_product_to_entity, to_product_search_builder
from Ecommerce.app.exception.http import ResourceNotFoundException
from Ecommerce.app.repository.CategoryRepository import CategoryRepository
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.repository.ProductRepository import ProductRepository
from Ecommerce.app.schemas.page import PageResponse
from Ecommerce.app.schemas.product import ProductResponse, ProductCreate, ProductUpdate, ProductSearchRequest


class ProductService:
    def __init__(
            self,
            product_repo: ProductRepository,
            category_repo: Optional[CategoryRepository] = None,
            user_repo: Optional[UserRepository] = None
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.user_repo = user_repo

    async def get_all_products(
            self,
            search_request : ProductSearchRequest,
            page: int,
            page_size: int
    ) -> PageResponse[ProductResponse]:
        product_search_builder = to_product_search_builder(search_request)

        items, total= await self.product_repo.get_products(product_search_builder, page, page_size)

        product_response_list: List[ProductResponse] = []
        for item in items:
            product_response = to_product_response(item)
            product_response_list.append(product_response)

        return PageResponse(
            items=product_response_list,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size else 1
        )

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        existing_category = await self.category_repo.get_category_by_id(data.category_id)
        if not existing_category:
            raise ResourceNotFoundException(f"Category with id '{data.category_id}' not found")
        existing_user = await self.user_repo.get_user_by_id(data.seller_id)
        if not existing_user:
            raise ResourceNotFoundException(f"User with id '{data.user_id}' not found")

        product = create_product_to_entity(data)
        saved_product = await self.product_repo.save(product)
        return to_product_response(saved_product)

    async def update_product(self, data: ProductUpdate, product_id: int) -> ProductResponse:
        existing_product = await self.product_repo.get_product_by_id(product_id)
        if not existing_product:
            raise ResourceNotFoundException(f"Product with id '{product_id}' not found")
        existing_category = await self.category_repo.get_category_by_id(data.category_id)
        if not existing_category:
            raise ResourceNotFoundException(f"Category with id '{data.category_id}' not found")
        existing_user = await self.user_repo.get_user_by_id(data.seller_id)
        if not existing_user:
            raise ResourceNotFoundException(f"User with id '{data.user_id}' not found")

        product = update_product_to_entity(existing_product, data)

        saved_product = await self.product_repo.save(product)
        return to_product_response(saved_product)

    async def delete_product(self, product_id: int) -> None:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(f"Product with id '{product_id}' not found")
        await self.product_repo.delete(product)