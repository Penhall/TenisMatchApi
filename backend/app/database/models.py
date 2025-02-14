# /backend/app/database/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

class TenisData(Base):
    __tablename__ = "tenis_data"

    id = Column(Integer, primary_key=True, index=True)
    tenis_estilo = Column(String, nullable=False)
    tenis_marca = Column(String, nullable=False)
    tenis_cores = Column(String, nullable=False)
    tenis_preco = Column(Float, nullable=False)
    match_success = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "tenis_estilo": self.tenis_estilo,
            "tenis_marca": self.tenis_marca,
            "tenis_cores": self.tenis_cores,
            "tenis_preco": self.tenis_preco,
            "match_success": self.match_success,
            "created_at": self.created_at.isoformat()
        }

class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    training_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "training_date": self.training_date.isoformat()
        }