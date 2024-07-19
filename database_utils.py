from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup import DATABASE_URL
from database import Base  # Adjust the import path based on your project structure

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)