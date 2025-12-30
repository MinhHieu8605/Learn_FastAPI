from Ecommerce.app.builder.ProductSearchBuilder import ProductSearchBuilder
from Ecommerce.app.enums import ProductStatus
from Ecommerce.app.models import Product
from Ecommerce.app.schemas.product import ProductResponse, ProductInDB, ProductCreate, ProductUpdate, \
    ProductSearchRequest


def to_product_response(product:Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        thumbnail=product.thumbnail,
        status=product.status,
        brand=product.brand,
        category_id=product.category_id,
        category_name=product.category.name,
        seller_id=product.seller_id,
        seller_name=product.seller.user_name
    )

def create_product_to_entity(data: ProductCreate) -> Product:
    return Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        thumbnail=data.thumbnail,
        brand=data.brand,
        status=data.status or ProductStatus.PENDING,
        category_id=data.category_id,
        seller_id=data.seller_id
    )

def update_product_to_entity(product: Product, data: ProductUpdate) -> Product:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    return product

def to_product_search_builder(request: ProductSearchRequest) -> ProductSearchBuilder:
    builder = ProductSearchBuilder.Builder()
    builder.set_name(request.name)
    builder.set_price_from(request.price_from)
    builder.set_price_to(request.price_to)
    builder.set_stock(request.stock)
    builder.set_stock_min(request.stock_min)
    builder.set_status(request.status)
    builder.set_category_id(request.category_id)
    builder.set_category_name(request.category_name)
    builder.set_seller_name(request.seller_name)
    builder.set_seller_id(request.seller_id)
    builder.set_brand(request.brand)
    return builder.build()
