from fastapi import FastAPI
from app.api.endpoints import auth, tickets
from app.utils.database import engine
from app.models.user import Base

# Initialize FastAPI application with project metadata
app = FastAPI(
    title="Customer Support Assistant",
    description="A backend for managing customer support tickets with AI integration",
    version="1.0.0"
)

# Event handler to create database tables on application startup
@app.on_event("startup")
async def startup_event():
    """
    Creates all database tables defined in SQLAlchemy models when the application starts.
    Uses async connection to ensure compatibility with async SQLAlchemy.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include API routers for authentication and ticket management
app.include_router(auth.router)
app.include_router(tickets.router)