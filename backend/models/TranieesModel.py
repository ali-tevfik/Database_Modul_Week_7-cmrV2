from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base,        relationship
from db.db import Base  # senin declarative_base'i aldığın yer


class Trainee(Base):
    __tablename__ = "trainees"
    trainee_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone_number = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    state = Column(String, nullable=True)
    application_period = Column(String, nullable=True)
    applications = relationship("Application", back_populates="trainee")
    mentors = relationship("Mentor", back_populates="trainee")
    updatedTime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project_tracking = relationship("ProjectTracking", back_populates="trainee")