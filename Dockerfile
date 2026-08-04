# Use official Python image
FROM python:3.12-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]