from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    blogs = relationship("Blog", back_populates="author")

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    body = Column(String)
    created_on = Column(DateTime)
    author = relationship("User", back_populates = "blogs")

    