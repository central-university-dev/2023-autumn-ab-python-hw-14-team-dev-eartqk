# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /opt/app

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

COPY . .

# Application entrypoint
CMD ["uvicorn", "src.social_network.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
