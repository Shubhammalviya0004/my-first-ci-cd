# Base image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy requirements (first step)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask App
CMD ["python", "app.py"]
