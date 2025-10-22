from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from db.db import Base  # senin declarative_base'i aldığın yer

class Application(Base):
    __tablename__ = "applications"
    application_id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(Integer, ForeignKey("trainees.trainee_id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    current_status = Column(String, nullable=True)
    wants_IT_training = Column(Boolean, default=False)
    economic_status = Column(String, nullable=True)
    attending_language_course = Column(Boolean, default=False)
    english_level = Column(String, nullable=True)
    dutch_level = Column(String, nullable=True)
    under_pressure = Column(Boolean, default=False)
    completed_bootcamp = Column(Boolean, default=False)
    online_IT_course = Column(Boolean, default=False)
    IT_experience = Column(Boolean, default=False)
    includes_project = Column(Boolean, default=False)
    wants_to_work = Column(Boolean, default=False)
    reason_for_participation = Column(String, nullable=True)
    application_period = Column(String, nullable=True)
    Cybersecurity_Powerplatform = Column(String, nullable=True)
    trainee = relationship("Trainee", back_populates="applications")