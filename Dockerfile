FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install & configure poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

# Install dependencies with poetry (excluding dev dependencies)
COPY pyproject.toml poetry.lock  ./
RUN poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of the application code into the container at /
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application using uvicorn
CMD poetry run uvicorn --host 0.0.0.0 app.app:app
