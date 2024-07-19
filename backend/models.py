from sqlalchemy import JSON, Boolean, create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from setup import DATABASE_URL, Base


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    data = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_ai = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class ModelConfiguration(Base):
    __tablename__ = "model_configurations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    configuration = Column(JSON)  # Stores configuration as JSON
    description = Column(String)

User.conversations = relationship("Conversation", back_populates="owner")
Conversation.messages = relationship("Message", back_populates="conversation")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)