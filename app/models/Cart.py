from decimal import Decimal
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from Ecommerce.app.db.base import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    user = relationship("User", back_populates="carts")

    cart_items = relationship("CartItem", back_populates="cart")

    @property
    def get_total_price(self) -> Decimal:
        total_price = Decimal("0")
        for cart_item in self.cart_items:
            unit_price = Decimal(str(cart_item.unit_price))
            quantity = cart_item.quantity
            total_price += unit_price * quantity
        return total_price