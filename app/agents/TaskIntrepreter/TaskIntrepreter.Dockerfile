# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy your Flask app code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask requests

# Expose the port
EXPOSE 7073

# Start the Flask app
CMD ["python", "interpreter_agent.py"]
