from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from Ecommerce.app.db.base import Base
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url = Column(String, nullable=False)

    product = relationship("Product", back_populates="product_images")