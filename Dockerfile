FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will override this)
EXPOSE $PORT

# Run the application with dynamic port
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} 