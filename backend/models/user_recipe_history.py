from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class UserRecipeHistory(BaseModel):
    """
    Tracks what recipes the user has cooked.
    """
    __tablename__ = "user_recipe_history"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    cooked_on = Column(DateTime, default=datetime.utcnow)
    rating = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    servings_made = Column(Integer, nullable=True)

    user = relationship("User", back_populates="recipe_history")
    recipe = relationship("Recipe", back_populates="user_history")

    def __repr__(self):
        return f"<UserRecipeHistory(id={self.id}, user_id={self.user_id}, recipe_id={self.recipe_id})>"
