from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TicketBase(BaseModel):
    """
    Base Pydantic model for ticket data.
    """
    title: str  # Ticket title
    description: str  # Ticket description

class TicketCreate(TicketBase):
    """
    Schema for creating a new ticket.
    """
    pass

class TicketOut(TicketBase):
    """
    Schema for ticket output, including additional fields.
    """
    id: UUID  # Unique ticket identifier
    status: str  # Ticket status
    created_at: datetime  # Creation timestamp
    user_id: UUID  # ID of the user who created the ticket

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility