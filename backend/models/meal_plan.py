import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Date, Enum, Float
from sqlalchemy.orm import relationship

from .base import BaseModel
from .recipe import MealType


class MealPlanStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class MealPlan(BaseModel):
    """
    Weekly/monthly meal plan for a user.
    """
    __tablename__ = "meal_plans"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    persons_count = Column(Integer, default=1)
    budget = Column(Float, nullable=True)
    status = Column(Enum(MealPlanStatus), default=MealPlanStatus.DRAFT)

    user = relationship("User", back_populates="meal_plans")
    entries = relationship("MealPlanEntry", back_populates="meal_plan", cascade="all, delete-orphan")
    shopping_lists = relationship("ShoppingList", back_populates="meal_plan")

    def __repr__(self):
        return f"<MealPlan(id={self.id}, title={self.title}, status={self.status.value})>"


class MealPlanEntry(BaseModel):
    """
    Individual day/meal slot in a plan.
    """
    __tablename__ = "meal_plan_entries"

    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    meal_type = Column(Enum(MealType), nullable=False)
    servings = Column(Integer, default=1)
    notes = Column(String(500), nullable=True)

    meal_plan = relationship("MealPlan", back_populates="entries")
    recipe = relationship("Recipe", back_populates="meal_plan_entries")

    def __repr__(self):
        return f"<MealPlanEntry(id={self.id}, date={self.scheduled_date}, meal={self.meal_type.value})>"
