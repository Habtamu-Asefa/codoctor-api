from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.auth.auth_utils import get_password_hash
from backend.models.setup import DATABASE_URL
from backend.models.schema import Base, User  # Adjust the import path based on your project structure

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_initial_user():
    db = SessionLocal()
    # Check if there are any users
    if not db.query(User).first():
        # No users found, create a new user
        new_user = User(
            username="default_user",
            email="user@example.com",
            hashed_password=get_password_hash("password"),
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print("Initial user created.")
    else:
        print("Users already exist.")
    db.close()


create_initial_user()

