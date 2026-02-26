import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from .base import BaseModel


class InventoryType(enum.Enum):
    INGREDIENT = "ingredient"
    UTENSIL = "utensil"


class GeneralInventoryCategory(BaseModel):
    """
    Categories for organizing inventory items.
    Examples: Dairy, Spices, Vegetables, Cookware.
    """
    __tablename__ = "general_inventory_categories"

    name = Column(String(100), nullable=False, unique=True)
    type = Column(Enum(InventoryType), nullable=False)
    description = Column(Text, nullable=True)

    items = relationship("GeneralInventoryItem", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<GeneralInventoryCategory(id={self.id}, name={self.name}, type={self.type.value})>"


class GeneralInventoryItem(BaseModel):
    """
    Master list of all possible items in the system.
    Loaded from CSV. Includes both ingredients and utensils.
    """
    __tablename__ = "general_inventory_items"

    name = Column(String(200), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("general_inventory_categories.id"), nullable=False)
    type = Column(Enum(InventoryType), nullable=False)
    image_url = Column(String(500), nullable=True)
    unit = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)

    category = relationship("GeneralInventoryCategory", back_populates="items")
    pantry_items = relationship("UserPantryItem", back_populates="item")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="item")
    recipe_utensils = relationship("RecipeUtensil", back_populates="item")
    shopping_list_items = relationship("ShoppingListItem", back_populates="item")

    def __repr__(self):
        return f"<GeneralInventoryItem(id={self.id}, name={self.name}, type={self.type.value})>"


class UserPantryItem(BaseModel):
    """
    What the user actually has in their pantry.
    Links user to general inventory items with quantity.
    """
    __tablename__ = "user_pantry_items"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("general_inventory_items.id"), nullable=False)
    quantity = Column(Float, default=0)
    unit = Column(String(50), nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="pantry_items")
    item = relationship("GeneralInventoryItem", back_populates="pantry_items")

    def __repr__(self):
        return f"<UserPantryItem(id={self.id}, user_id={self.user_id}, item={self.item_id}, qty={self.quantity})>"
