from databases import Database
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

Base = declarative_base()