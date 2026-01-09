# Use an official Python runtime as a parent image
FROM python:3.13-slim-trixie

# Download the latest installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /usr/src/app

# Install required system dependencies, including gcc and other build tools
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

ENV UV_NO_DEV=1

# Install any needed packages specified 
RUN uv sync --locked

# Expose the application's port
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
# CMD ["python", "./app.py"]
CMD ["uv", "run", "app.py"]
