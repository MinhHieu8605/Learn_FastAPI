from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from Ecommerce.app.db.base import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE",))

    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
