# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential libssl-dev libffi-dev python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only the lock & project metadata first (for better cache)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without dev packages
RUN poetry install --no-root --only main

# Copy the rest of the application
COPY . /app/

# Install the app (if it's a package)
RUN poetry install --only main

# Run the app
CMD ["poetry", "run", "python", "app/main.py"]

