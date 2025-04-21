from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from app.models.message import Message
from app.schemas.ticket import TicketCreate
from app.schemas.message import MessageCreate
from app.models.user import User
from fastapi import HTTPException, status

class TicketService:
    """
    Service class for managing ticket and message operations.
    """
    async def create_ticket(self, ticket_data: TicketCreate, user: User, db: AsyncSession):
        """
        Create a new support ticket for the authenticated user.
        
        Args:
            ticket_data: Ticket creation data (title, description).
            user: Authenticated user.
            db: Async database session.
        
        Returns:
            Created ticket object.
        """
        ticket = Ticket(**ticket_data.dict(), user_id=user.id)
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    async def get_tickets(self, user: User, db: AsyncSession):
        """
        Retrieve all tickets for the authenticated user.
        
        Args:
            user: Authenticated user.
            db: Async database session.
        
        Returns:
            List of ticket objects.
        """
        result = await db.execute(select(Ticket).filter(Ticket.user_id == user.id))
        return result.scalars().all()

    async def get_ticket(self, ticket_id: UUID, user: User, db: AsyncSession):
        """
        Retrieve a specific ticket by ID, ensuring it belongs to the user.
        
        Args:
            ticket_id: UUID of the ticket.
            user: Authenticated user.
            db: Async database session.
        
        Returns:
            Ticket object.
        
        Raises:
            HTTPException: If ticket is not found or doesn't belong to the user.
        """
        result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id, Ticket.user_id == user.id))
        ticket = result.scalars().first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket

    async def add_message(self, ticket_id: UUID, message_data: MessageCreate, user: User, db: AsyncSession):
        """
        Add a message to a specific ticket.
        
        Args:
            ticket_id: UUID of the ticket.
            message_data: Message creation data (content).
            user: Authenticated user.
            db: Async database session.
        
        Returns:
            Created message object.
        """
        ticket = await self.get_ticket(ticket_id, user, db)
        message = Message(**message_data.dict(), ticket_id=ticket.id)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message