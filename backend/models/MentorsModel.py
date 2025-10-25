from sqlalchemy import Column, Integer, String, DateTime, Boolean,func,ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from db.db import Base  # senin declarative_base'i aldığın yer




class Mentor(Base):
    __tablename__ = "mentors"
    mentor_id = Column(Integer, primary_key=True, index=True)
    meeting_date = Column(DateTime, nullable=True)
    full_name = Column(String, nullable=False)
    trainee_id = Column(Integer, ForeignKey("trainees.trainee_id"), nullable=True)
    has_knowledge = Column(Boolean, default=False)
    can_join_VIT_project = Column(Boolean, default=False)
    opinion = Column(String, nullable=True)
    workload = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    updatedTime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    trainee = relationship("Trainee", back_populates="mentors")
