from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, Token
from app.services.auth import AuthService
from app.utils.database import get_db

# Initialize API router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user and return a JWT token.
    
    Args:
        user_data: User creation data (email, password).
        db: Async database session.
    
    Returns:
        Token response with JWT and token type.
    """
    user = await auth_service.register(user_data, db)
    token = await auth_service.login(user_data.email, user_data.password, db)
    return token

@router.post("/login", response_model=Token)
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.
    
    Args:
        email: User email.
        password: Plain-text password.
        db: Async database session.
    
    Returns:
        Token response with JWT and token type.
    """
    return await auth_service.login(email, password, db)