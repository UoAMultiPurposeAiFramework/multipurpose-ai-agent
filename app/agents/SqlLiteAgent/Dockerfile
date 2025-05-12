FROM python:3.10-slim

WORKDIR /app

# Copy entire SqlLiteAgent project into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask openai python-dotenv httpx

# Optional: Set up database (comment if DB already exists)
RUN python setup_db.py

EXPOSE 7070

CMD ["python", "agent1.py"]
