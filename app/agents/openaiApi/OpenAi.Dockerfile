FROM python:3.10-slim
WORKDIR /app

# Copy your source code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask openai==1.78.0 python-dotenv

# Expose the Flask port
EXPOSE 7072

# Run your Flask app (replace with your script name)
CMD ["python", "openai_proxy.py"]