from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    """
    Base Pydantic model for user data.
    """
    email: EmailStr  # Validated email address

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str  # Plain-text password (will be hashed)

class UserOut(UserBase):
    """
    Schema for user output, including additional fields.
    """
    id: UUID  # Unique user identifier
    role: str  # User role (e.g., user, admin)

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility

class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str  # JWT token
    token_type: str  # Token type (e.g., bearer)