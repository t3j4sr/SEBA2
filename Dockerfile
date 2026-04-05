FROM python:3.11-slim

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from the backend folder
COPY SEBA/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repository into the container
COPY . /app

# Set working directory to the API backend
WORKDIR /app/SEBA

# Render automatically provides a $PORT variable, so we pass it safely to uvicorn
CMD if [ -z "$PORT" ]; then PORT=8000; fi; uvicorn main:app --host 0.0.0.0 --port $PORT
