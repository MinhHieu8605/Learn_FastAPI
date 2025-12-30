from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from Ecommerce.app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    status = Column(Integer, nullable=False, server_default="1")
    address = Column(String)
    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    roles = relationship(
        "Role",
        secondary="user_roles",
        viewonly=True
    )
    carts = relationship("Cart", back_populates="user")
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    orders = relationship("Order", back_populates="user")
    products = relationship(
        "Product",
        back_populates="seller",
        cascade="all, delete-orphan"
    )
