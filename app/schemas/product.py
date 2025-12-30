from typing import List, Optional

from pydantic import BaseModel, Field

from Ecommerce.app.enums.ProductStatus import ProductStatus


class ProductImageBase(BaseModel):
    image_url: str

    class Config:
        from_attributes = True


class ProductImage(ProductImageBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    thumbnail: str
    brand: str
    status: ProductStatus = ProductStatus.PENDING
    category_id: int
    seller_id: int
    category_name: str
    seller_name: str

    class Config:
        from_attributes = True

class ProductSearchRequest(BaseModel):
    name: Optional[str] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None
    stock: Optional[int] = None
    stock_min: Optional[int] = None
    status: Optional[ProductStatus] = None
    category_id: Optional[int] = None
    seller_id: Optional[int] = None
    category_name: Optional[str] = None
    seller_name: Optional[str] = None
    brand: Optional[str] = None


class ProductCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    thumbnail: Optional[str] = None
    brand: Optional[str] = None
    status: Optional[ProductStatus] = None
    category_id: Optional[int] = None
    seller_id: Optional[int] = None
    image_urls: List[str] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    thumbnail: Optional[str] = None
    brand: Optional[str] = None
    status: Optional[ProductStatus] = None
    category_id: Optional[int] = None
    seller_id: Optional[int] = None


class ProductInDB(ProductBase):
    id: int
    class Config:
        from_attributes = True


class ProductResponse(ProductInDB):
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    message: str
    data: List[ProductInDB]

    class Config:
        from_attributes = True
