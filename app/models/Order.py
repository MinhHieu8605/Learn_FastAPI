from Ecommerce.app.db.base import Base
from sqlalchemy import Column, Integer, DateTime, DECIMAL, Enum, ForeignKey
from Ecommerce.app.enums.OrderStatus import OrderStatus
from Ecommerce.app.enums.PaymentStatus import PaymentStatus
from sqlalchemy.orm import relationship
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    total_price = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    order_date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")

    order_items = relationship(
        "OrderItems",
        back_populates="order",
        cascade="all, delete-orphan"
    )
