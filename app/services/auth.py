from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    """
    Service class for handling authentication-related operations.
    """
    async def register(self, user_data: UserCreate, db: AsyncSession):
        """
        Register a new user with hashed password.
        
        Args:
            user_data: User creation data (email, password).
            db: Async database session.
        
        Returns:
            Created user object.
        
        Raises:
            HTTPException: If email is already registered.
        """
        result = await db.execute(select(User).filter(User.email == user_data.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(user_data.password)
        user = User(email=user_data.email, hashed_password=hashed_password, role="user")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def login(self, email: str, password: str, db: AsyncSession):
        """
        Authenticate a user and generate a JWT token.
        
        Args:
            email: User email.
            password: Plain-text password.
            db: Async database session.
        
        Returns:
            Dictionary containing JWT token and token type.
        
        Raises:
            HTTPException: If credentials are invalid.
        """
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}