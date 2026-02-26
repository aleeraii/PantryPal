import enum

from sqlalchemy import Column, String, Integer, Text, Enum, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class RecipeSource(enum.Enum):
    AI_GENERATED = "ai_generated"
    DATABASE = "database"
    USER_SUBMITTED = "user_submitted"


class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class Recipe(BaseModel):
    """
    Recipe model - can be AI-generated or seeded from database.
    """
    __tablename__ = "recipes"

    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    cuisine_type = Column(String(50), nullable=True)
    meal_type = Column(Enum(MealType), nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    servings = Column(Integer, default=1)
    estimated_cost = Column(Float, nullable=True)
    dietary_tags = Column(JSON, default=list)
    source = Column(Enum(RecipeSource), default=RecipeSource.DATABASE)
    image_url = Column(String(500), nullable=True)

    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    utensils = relationship("RecipeUtensil", back_populates="recipe", cascade="all, delete-orphan")
    user_history = relationship("UserRecipeHistory", back_populates="recipe")
    meal_plan_entries = relationship("MealPlanEntry", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe(id={self.id}, title={self.title}, source={self.source.value})>"


class RecipeIngredient(BaseModel):
    """
    Junction between recipe and inventory items (ingredients).
    """
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("general_inventory_items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    is_optional = Column(Boolean, default=False)
    notes = Column(String(200), nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    item = relationship("GeneralInventoryItem", back_populates="recipe_ingredients")

    def __repr__(self):
        return f"<RecipeIngredient(recipe_id={self.recipe_id}, item_id={self.item_id}, qty={self.quantity})>"


class RecipeUtensil(BaseModel):
    """
    Which utensils a recipe needs.
    """
    __tablename__ = "recipe_utensils"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("general_inventory_items.id"), nullable=False)
    is_optional = Column(Boolean, default=False)
    notes = Column(String(200), nullable=True)

    recipe = relationship("Recipe", back_populates="utensils")
    item = relationship("GeneralInventoryItem", back_populates="recipe_utensils")

    def __repr__(self):
        return f"<RecipeUtensil(recipe_id={self.recipe_id}, item_id={self.item_id})>"
