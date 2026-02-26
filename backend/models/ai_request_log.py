from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class AIRequestLog(BaseModel):
    """
    Logs every AI call for cost tracking and caching.
    prompt_hash allows returning cached recipes if someone with
    the same ingredients asks again, saving API costs.
    """
    __tablename__ = "ai_request_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt_hash = Column(String(64), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    model_used = Column(String(50), nullable=False)
    tokens_used = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    request_type = Column(String(50), nullable=True)
    status = Column(String(20), default="success")
    error_message = Column(Text, nullable=True)

    user = relationship("User", back_populates="ai_request_logs")

    def __repr__(self):
        return f"<AIRequestLog(id={self.id}, user_id={self.user_id}, model={self.model_used})>"
