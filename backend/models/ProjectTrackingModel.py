from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from db.db import Base  # senin declarative_base'i aldığın yer



class ProjectTracking(Base):
    __tablename__ = "project_tracking"
    project_tracking_id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.trainee_id"), nullable=False)
    project_submission_date = Column(DateTime, nullable=True)
    project_progress_date = Column(DateTime, nullable=True)

    trainee = relationship("Trainee", back_populates="project_tracking")