from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from Ecommerce.app.api.deps import require_roles
from Ecommerce.app.constant.SystemConstant import SystemConstant
from Ecommerce.app.core.deps import get_db
from Ecommerce.app.repository.CategoryRepository import CategoryRepository
from Ecommerce.app.repository.ProductRepository import ProductRepository
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.schemas.page import PageResponse
from Ecommerce.app.schemas.product import ProductResponse, ProductUpdate, ProductCreate, ProductSearchRequest
from Ecommerce.app.services.ProductService import ProductService

router = APIRouter()

@router.get("/", response_model=PageResponse[ProductResponse])
async def get_all_products(
    search_request: ProductSearchRequest = Depends(),
    db:AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([SystemConstant.ADMIN_ROLE])),
    page: int = 1,
    page_size: int = 10
):
    service = ProductService(
        ProductRepository(db)
    )
    return await service.get_all_products(search_request, page, page_size)

@router.post("/",
             response_model=ProductResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create new product",
             response_description="Product created successfully")
async def create_product(
    product: ProductCreate,
    db:AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([SystemConstant.ADMIN_ROLE]))
):
    service = ProductService(
        ProductRepository(db),
        CategoryRepository(db),
        UserRepository(db)
    )
    return await service.create_product(product)

@router.put("/{product_id}",
            response_model=ProductResponse,
            status_code=status.HTTP_200_OK,
            summary="Update product",
            response_description="Product updated successfully")
async def update_product(
    product_id: int,
    product : ProductUpdate,
    db:AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([SystemConstant.ADMIN_ROLE]))
):
    service = ProductService(
        ProductRepository(db),
        CategoryRepository(db),
        UserRepository(db)
    )
    return await service.update_product(product, product_id)

@router.delete("/product_id",
               status_code=status.HTTP_200_OK,
               summary="Delete product",
               response_description="Product deleted successfully")
async def delete_product(
    product_id: int,
    db:AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([SystemConstant.ADMIN_ROLE]))
):
    service = ProductService(ProductRepository(db))
    await service.delete_product(product_id)
    return {"message": "Product has been successfully deleted (soft delete)."}