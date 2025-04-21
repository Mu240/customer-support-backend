from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    """
    Base Pydantic model for message data.
    """
    content: str  # Message content

class MessageCreate(MessageBase):
    """
    Schema for creating a new message.
    """
    pass

class MessageOut(MessageBase):
    """
    Schema for message output, including additional fields.
    """
    id: UUID  # Unique message identifier
    is_ai: bool  # Indicates if message is AI-generated
    created_at: datetime  # Creation timestamp
    ticket_id: UUID  # ID of the associated ticket

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility