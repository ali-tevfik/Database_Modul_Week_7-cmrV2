from sqlalchemy import Column, Integer, String
from db.db import Base  # senin declarative_base'i aldığın yer

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=True)
