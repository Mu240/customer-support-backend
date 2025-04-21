Customer Support Assistant Backend
A FastAPI-based backend for a customer support assistant, featuring user authentication, support ticket management, and real-time AI response generation using the Groq API.
Setup Instructions
Prerequisites

Python 3.11+
Poetry (for dependency management)
Docker and Docker Compose
PostgreSQL (included in Docker Compose)
Groq API key (obtain from Groq Console)

Installation Steps

Clone the repository:
git clone https://github.com/Mu240/customer-support-backend.git
cd customer-support-backend


Install Poetry:
pip install poetry


Install dependencies:
poetry install


Configure environment variables:Copy .env.example to .env and update with your values:
cp .env.example .env

Edit .env to include:
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/customer_support
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key


Run the application with Docker:
docker-compose up --build


Apply database migrations:In a new terminal, run:
poetry run alembic upgrade head


Access the API:The API is available at http://localhost:8000. Explore endpoints using the interactive Swagger UI at http://localhost:8000/docs.


Running Locally (without Docker)

Ensure PostgreSQL is running locally and update DATABASE_URL in .env.
Install dependencies: poetry install.
Apply migrations: poetry run alembic upgrade head.
Start the server: poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload.

Architectural Decisions
Technology Stack

FastAPI: Chosen for its async support, automatic OpenAPI documentation, and dependency injection system, ideal for building performant APIs.
SQLAlchemy (Async): Used for ORM with async support, enabling efficient database operations with PostgreSQL.
Pydantic: Leveraged for data validation and serialization, ensuring type safety and clean API schemas.
Groq API: Integrated for AI-driven customer support responses, with streaming support for real-time feedback.
Docker: Used for containerization, ensuring consistent environments and easy deployment.

OOP Principles Applied

Encapsulation: Business logic is encapsulated in service classes (AuthService, TicketService, AIService), hiding implementation details.
Single Responsibility Principle: Each module (services, models, schemas) has a single responsibility, improving maintainability.
Dependency Injection: FastAPI’s Depends system injects dependencies like database sessions and authenticated users, enhancing testability.
Modularity: The codebase is organized into packages (api, core, models, schemas, services, utils) for clear separation of concerns.

Project Structure

api/endpoints/: Contains API route definitions.
api/dependencies/: Defines reusable dependencies (e.g., authentication).
core/: Stores configuration and settings.
models/: Defines SQLAlchemy database models.
schemas/: Contains Pydantic schemas for data validation.
services/: Implements business logic using service classes.
utils/: Provides utility functions (e.g., JWT handling, database setup).
migrations/: Manages database schema migrations with Alembic.

Design Patterns Used

Service Layer Pattern:

Why: Encapsulates business logic in service classes (AuthService, TicketService, AIService), separating it from API routes and database operations. This improves testability and maintainability.
Implementation: Each service handles specific operations (e.g., AuthService for authentication, TicketService for ticket management), interacting with models and schemas.


Repository Pattern:

Why: Abstracts database operations, making it easier to swap out the database layer or mock it for testing.
Implementation: Services act as repositories, using SQLAlchemy to perform CRUD operations on models.


Dependency Injection:

Why: Promotes loose coupling and testability by injecting dependencies at runtime.
Implementation: FastAPI’s Depends injects database sessions (get_db) and authenticated users (get_current_user).



Challenges Faced and Solutions

Async SQLAlchemy Integration:

Challenge: Configuring SQLAlchemy for async operations with PostgreSQL was complex, especially with Alembic migrations.
Solution: Used sqlalchemy.ext.asyncio for async engine and sessions, and modified Alembic’s env.py to support async connections.


Streaming AI Responses:

Challenge: Implementing Server-Sent Events (SSE) for real-time AI responses required handling async streaming from the Groq API.
Solution: Used FastAPI’s StreamingResponse with an async generator from AsyncGroq, ensuring chunks are streamed efficiently.


JWT Authentication:

Challenge: Ensuring secure JWT generation and validation with role-based access control.
Solution: Used python-jose for JWT handling and implemented a dependency (get_current_user) to validate tokens and retrieve user roles.



Potential Improvements with More Time

Testing:

Add unit tests for services and integration tests for API endpoints using pytest and pytest-asyncio.
Mock database and Groq API calls for isolated testing.


Rate Limiting:

Implement rate limiting using slowapi to prevent abuse of AI response endpoints.


Enhanced Prompt System:

Develop a more sophisticated prompt template system with dynamic variables and context management.


Caching:

Use Redis to cache frequently accessed tickets or AI responses, improving performance.


Logging:

Add structured logging with structlog to track API usage and errors.



API Endpoints



Method
Endpoint
Description



POST
/auth/signup
Register a new user


POST
/auth/login
Login and receive a JWT token


GET
/tickets
List all tickets for the authenticated user


POST
/tickets
Create a new support ticket


GET
/tickets/{ticket_id}
Retrieve details of a specific ticket


POST
/tickets/{ticket_id}/messages
Add a message to a ticket


GET
/tickets/{ticket_id}/ai-response
Stream an AI-generated response (SSE)


Running Tests

Run linters and type checkers:poetry run black .
poetry run isort .
poetry run mypy .


Run tests (if implemented):poetry run pytest




