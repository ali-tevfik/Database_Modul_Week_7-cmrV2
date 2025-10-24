from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database



DATABASE_URL = "postgresql+psycopg2://postgres:19Ekim88@localhost:5432/crm_db"




engine = create_engine(DATABASE_URL) 
if not database_exists(engine.url):
    create_database(engine.url)
    print("Created DB ✅")
    
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
