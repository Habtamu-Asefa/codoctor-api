from sqlalchemy import JSON, Boolean, create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
<<<<<<< HEAD:backend/models/schema.py
from backend.models.setup import DATABASE_URL, Base

import enum


class UserRole(enum.Enum):
    admin = "Admin"
    doctor = "Doctor"
    patient = "Patient"
=======
from setup import DATABASE_URL, Base
from sqlalchemy.orm import Session
>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220:backend/models.py


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    messages = relationship("Message", back_populates="conversation")
    owner = relationship("User", back_populates="conversations")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    data = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_ai = Column(Boolean, default=False)
    conversation = relationship("Conversation", back_populates="messages")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True,unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
<<<<<<< HEAD:backend/models/schema.py
    role = Column(Enum(UserRole), default=UserRole.doctor)
    conversations = relationship("Conversation", back_populates="owner")
    # for now by default all users are doctors
=======
    conversations = relationship("Conversation", back_populates="owner")

>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220:backend/models.py

class ModelConfiguration(Base):
    __tablename__ = "model_configurations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    configuration = Column(JSON)  # Stores configuration as JSON
    description = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)