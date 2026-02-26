from sqlalchemy import Column, String, Integer, Text, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """
    User model with device-based identification.
    No traditional auth - uses device UUID sent via X-Device-ID header.
    """
    __tablename__ = "users"

    device_id = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    household_size = Column(Integer, default=1)
    monthly_budget = Column(Integer, nullable=True)
    currency = Column(String(3), default="USD")
    dietary_preferences = Column(JSON, default=list)

    pantry_items = relationship("UserPantryItem", back_populates="user", cascade="all, delete-orphan")
    recipe_history = relationship("UserRecipeHistory", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    shopping_lists = relationship("ShoppingList", back_populates="user", cascade="all, delete-orphan")
    ai_request_logs = relationship("AIRequestLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, device_id={self.device_id}, name={self.name})>"
