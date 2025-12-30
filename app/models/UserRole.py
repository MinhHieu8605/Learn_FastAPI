from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Ecommerce.app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="users")
