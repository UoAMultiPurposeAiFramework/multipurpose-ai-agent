FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 7071

# Run the Flask app
CMD ["python", "agent2.py"]
