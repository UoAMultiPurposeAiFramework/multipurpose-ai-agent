FROM python:3.10.13-slim

# Mark the role played by this container as ReAct Agent
EXPOSE 7788

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into container at /app
COPY ./im_server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./im_server ./
COPY ./common ./common
COPY ./configs/ ./configs

# Set the entry point for running the test_react_agent python file
ENTRYPOINT [ "python", "app.py" ]