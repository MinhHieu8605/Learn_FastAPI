from Ecommerce.app.db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)

    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")