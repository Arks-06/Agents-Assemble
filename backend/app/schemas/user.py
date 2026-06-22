# Defines the structure for user data validation and transformation.
# Enforces constraints for user registration inputs and data serialization for responses.

from pydantic import BaseModel, EmailStr, Field
from app.models.core import RoleEnum

# What is expected of the user
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

# What is safely returned to the user
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models