from sqlalchemy import Column, String, UUID, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base

class Ticket(Base):
    """
    SQLAlchemy model for the tickets table.
    Represents a customer support ticket with description and status.
    """
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)  # Ticket title
    description = Column(String, nullable=False)  # Ticket description
    status = Column(String, default="open")  # Ticket status (e.g., open, closed)
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation timestamp

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Foreign key to user
    user = relationship("User", back_populates="tickets")  # Relationship to user
    messages = relationship("Message", back_populates="ticket")  # One-to-many with messages