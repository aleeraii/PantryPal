import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, Float, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class ShoppingListStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ShoppingList(BaseModel):
    """
    Auto-generated shopping list from a meal plan.
    Based on what the user is missing in their pantry.
    """
    __tablename__ = "shopping_lists"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=True)
    title = Column(String(200), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(ShoppingListStatus), default=ShoppingListStatus.PENDING)
    estimated_total = Column(Float, nullable=True)

    user = relationship("User", back_populates="shopping_lists")
    meal_plan = relationship("MealPlan", back_populates="shopping_lists")
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ShoppingList(id={self.id}, user_id={self.user_id}, status={self.status.value})>"


class ShoppingListItem(BaseModel):
    """
    Individual item in a shopping list.
    """
    __tablename__ = "shopping_list_items"

    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("general_inventory_items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    is_purchased = Column(Boolean, default=False)
    estimated_price = Column(Float, nullable=True)
    notes = Column(String(200), nullable=True)

    shopping_list = relationship("ShoppingList", back_populates="items")
    item = relationship("GeneralInventoryItem", back_populates="shopping_list_items")

    def __repr__(self):
        return f"<ShoppingListItem(id={self.id}, item_id={self.item_id}, purchased={self.is_purchased})>"
