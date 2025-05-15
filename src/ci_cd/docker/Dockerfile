# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app/src/brief_app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/src/ci_cd/shell/app_entrypoint.sh

# Use the entrypoint script to start the application
ENTRYPOINT ["/app/src/ci_cd/shell/app_entrypoint.sh"]
