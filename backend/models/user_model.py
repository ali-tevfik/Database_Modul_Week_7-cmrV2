from sqlalchemy import Column, Integer, String,func,DateTime
from db.db import Base  # senin declarative_base'i aldığın yer

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    updatedTime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    role = Column(String, nullable=True)
