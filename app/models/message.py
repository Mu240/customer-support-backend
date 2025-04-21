from sqlalchemy import Column, String, UUID, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base

class Message(Base):
    """
    SQLAlchemy model for the messages table.
    Represents a message in a ticket, either from a user or AI.
    """
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)  # Message content
    is_ai = Column(Boolean, default=False)  # Flag to indicate if message is AI-generated
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation timestamp

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))  # Foreign key to ticket
    ticket = relationship("Ticket", back_populates="messages")  # Relationship to ticket