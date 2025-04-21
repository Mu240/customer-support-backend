from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the users table.
    Represents a user with authentication and role information.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)  # Unique email for login
    hashed_password = Column(String, nullable=False)  # Hashed password for security
    role = Column(String, default="user")  # User role (e.g., user, admin)

    # One-to-many relationship with tickets
    tickets = relationship("Ticket", back_populates="user")