# Use the official slim Python image as the base
FROM python:3.12-slim

# Define build-time metadata
ARG COMMIT_SHA=unknown
ARG BUILD_TIME=unknown

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy app source code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Save build metadata into a version file
RUN echo "Commit: $COMMIT_SHA" > /app/version.txt && \
    echo "Built at: $BUILD_TIME" >> /app/version.txt

# Make entrypoint executable
RUN chmod +x /app/src/ci_cd/shell/app_entrypoint.sh

# Expose app port
EXPOSE 8000

# Use exec form for entrypoint to properly receive signals
ENTRYPOINT ["/app/src/ci_cd/shell/app_entrypoint.sh"]
