from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ticket import TicketCreate, TicketOut
from app.schemas.message import MessageCreate, MessageOut
from app.services.ticket import TicketService
from app.services.ai import AIService
from app.utils.database import get_db
from app.models.user import User
from app.api.dependencies.auth import get_current_user
from uuid import UUID
from typing import List

# Initialize API router for ticket-related endpoints
router = APIRouter(prefix="/tickets", tags=["tickets"])
ticket_service = TicketService()
ai_service = AIService()

@router.post("/", response_model=TicketOut)
async def create_ticket(
    ticket_data: TicketCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new support ticket for the authenticated user.
    
    Args:
        ticket_data: Ticket creation data (title, description).
        user: Authenticated user (injected via dependency).
        db: Async database session.
    
    Returns:
        Created ticket details.
    """
    return await ticket_service.create_ticket(ticket_data, user, db)

@router.get("/", response_model=List[TicketOut])
async def get_tickets(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all tickets for the authenticated user.
    
    Args:
        user: Authenticated user (injected via dependency).
        db: Async database session.
    
    Returns:
        List of ticket details.
    """
    return await ticket_service.get_tickets(user, db)

@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve details of a specific ticket.
    
    Args:
        ticket_id: UUID of the ticket.
        user: Authenticated user (injected via dependency).
        db: Async database session.
    
    Returns:
        Ticket details.
    """
    return await ticket_service.get_ticket(ticket_id, user, db)

@router.post("/{ticket_id}/messages", response_model=MessageOut)
async def add_message(
    ticket_id: UUID,
    message_data: MessageCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a message to a specific ticket.
    
    Args:
        ticket_id: UUID of the ticket.
        message_data: Message creation data (content).
        user: Authenticated user (injected via dependency).
        db: Async database session.
    
    Returns:
        Created message details.
    """
    return await ticket_service.add_message(ticket_id, message_data, user, db)

@router.get("/{ticket_id}/ai-response")
async def stream_ai_response(
    ticket_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Stream an AI-generated response for a ticket using Server-Sent Events (SSE).
    
    Args:
        ticket_id: UUID of the ticket.
        user: Authenticated user (injected via dependency).
        db: Async database session.
    
    Returns:
        StreamingResponse with AI response chunks.
    """
    await ticket_service.get_ticket(ticket_id, user, db)  # Verify ticket exists
    return StreamingResponse(
        ai_service.generate_response(str(ticket_id), db),
        media_type="text/event-stream"
    )