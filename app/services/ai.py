from groq import AsyncGroq
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from app.models.message import Message
from app.core.config import settings
import json

class AIService:
    """
    Service class for generating AI responses using the Groq API.
    """
    def __init__(self):
        """
        Initialize the Groq client with the API key from settings.
        """
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def generate_response(self, ticket_id: str, db: AsyncSession):
        """
        Generate a streaming AI response for a ticket based on its description and message history.
        
        Args:
            ticket_id: UUID of the ticket.
            db: Async database session.
        
        Yields:
            JSON-encoded chunks of the AI response.
        
        Raises:
            HTTPException: If the ticket is not found.
        """
        # Retrieve ticket
        result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
        ticket = result.scalars().first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Retrieve message history
        result = await db.execute(select(Message).filter(Message.ticket_id == ticket_id))
        messages = result.scalars().all()
        message_history = "\n".join([f"{'AI' if msg.is_ai else 'User'}: {msg.content}" for msg in messages])
        latest_message = messages[-1].content if messages else ""

        # Construct prompt for AI
        prompt = f"""
        You are a helpful customer support assistant.
        The customer has the following issue: {ticket.description}

        Previous messages:
        {message_history}

        Customer's latest message: {latest_message}

        Provide a helpful response that addresses their concern:
        """

        # Accumulate response content for persistence
        full_content = ""
        async for chunk in self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            stream=True
        ):
            content = chunk.choices[0].delta.content or ""
            if content:
                full_content += content
                yield json.dumps({"content": content})

        # Save AI response to database
        if full_content:
            ai_message = Message(content=full_content, is_ai=True, ticket_id=ticket.id)
            db.add(ai_message)
            await db.commit()