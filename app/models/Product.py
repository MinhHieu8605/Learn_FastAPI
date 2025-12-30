from Ecommerce.app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, Boolean, TIMESTAMP, Enum
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from Ecommerce.app.enums.ProductStatus import ProductStatus
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    thumbnail = Column(String, nullable=False)
    status = Column(Enum(ProductStatus), nullable=False, server_default="PENDING")
    brand = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    category = relationship("Category", back_populates="products")
    seller = relationship("User", back_populates="products")

    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

    order_items = relationship("OrderItems", back_populates="product")

    product_images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )