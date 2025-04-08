from sqlalchemy import Column, JSON, DateTime, Enum, text
from sqlalchemy.dialects.mysql import INTEGER, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True, comment="UUID")
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    oauth_token = Column(JSON)
    created_at = Column(DateTime(6), server_default=text("CURRENT_TIMESTAMP(6)"))
    updated_at = Column(DateTime(6), server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"))

class Event(Base):
    __tablename__ = "events"
    
    id = Column(INTEGER(unsigned=True), primary_key=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime(6), nullable=False)
    end_time = Column(DateTime(6), nullable=False)
    location = Column(JSON)
    user_id = Column(CHAR(36), nullable=False)
    calendar_type = Column(Enum('primary', 'google', 'icloud'), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(6), server_default=text("CURRENT_TIMESTAMP(6)"))
    updated_at = Column(DateTime(6), server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"))