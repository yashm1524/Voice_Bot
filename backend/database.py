from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

URL_DATABASE = "sqlite:///./voicebot.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Float)

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True, index=True)
    answer = Column(String)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    account_number = Column(String, unique=True)
    email = Column(String)
    phone = Column(String)
    balance = Column(Float)
    account_type = Column(String)  # e.g., "Savings", "Checking"
    status = Column(String)

Base.metadata.create_all(bind=engine)
