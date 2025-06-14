from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    customer = relationship("Customer", back_populates="users", uselist=False)
class Customer(Base):
    __tablename__="customer"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String)
    users = relationship("Users", back_populates="customer")