from typing import Optional

from Ecommerce.app.enums.ProductStatus import ProductStatus


class ProductSearchBuilder:
    def __init__(self, builder: Builder):
        self.name = builder.name
        self.price_from = builder.price_from
        self.price_to = builder.price_to
        self.stock = builder.stock
        self.stock_min = builder.stock_min
        self.status = builder.status
        self.category_id = builder.category_id
        self.category_name = builder.category_name
        self.seller_name = builder.seller_name
        self.seller_id = builder.seller_id
        self.brand = builder.brand

    class Builder:
        def __init__(self):
            self.name : Optional[str] = None
            self.price_from : Optional[float] = None
            self.price_to : Optional[float] = None
            self.stock : Optional[int] = None
            self.stock_min : Optional[int] = None
            self.status : Optional[ProductStatus] = None
            self.category_id : Optional[int] = None
            self.category_name : Optional[str] = None
            self.seller_name : Optional[str] = None
            self.seller_id : Optional[int] = None
            self.brand : Optional[str] = None

        def set_name(self, name : str) -> ProductSearchBuilder.Builder:
            self.name = name
            return self

        def set_price_from(self, price_from : float) -> ProductSearchBuilder.Builder:
            self.price_from = price_from
            return self
        def set_price_to(self, price_to : float) -> ProductSearchBuilder.Builder:
            self.price_to = price_to
            return self
        def set_stock(self, stock : int) -> ProductSearchBuilder.Builder:
            self.stock = stock
            return self
        def set_stock_min(self, stock_min : int) -> ProductSearchBuilder.Builder:
            self.stock_min = stock_min
            return self
        def set_status(self, status : ProductStatus) -> ProductSearchBuilder.Builder:
            self.status = status
            return self
        def set_category_id(self, category_id : int) -> ProductSearchBuilder.Builder:
            self.category_id = category_id
            return self
        def set_category_name(self, category_name : str) -> ProductSearchBuilder.Builder:
            self.category_name = category_name
            return self
        def set_seller_name(self, seller_name : str) -> ProductSearchBuilder.Builder:
            self.seller_name = seller_name
            return self
        def set_seller_id(self, seller_id : int) -> ProductSearchBuilder.Builder:
            self.seller_id = seller_id
            return self
        def set_brand(self, brand : str) -> ProductSearchBuilder.Builder:
            self.brand = brand
            return self

        def build(self) -> ProductSearchBuilder:
            return ProductSearchBuilder(self)