from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Ecommerce.app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    street = Column(String, nullable=False)
    district = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    zipcode = Column(String(100))
    recipient_name = Column(String(100))
    phone_number = Column(String(20), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")