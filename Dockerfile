# Stage 1: Build Stage
FROM python:3.9-slim AS build

# Set environment variables to avoid Python writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Production Stage
FROM python:3.9-slim AS production

# Set environment variables to avoid Python writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set a non-root user for security
RUN useradd -m appuser
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy only necessary files from the build stage to the production image
COPY --from=build /app /app

# Expose the port the app runs on
EXPOSE 5000

# Install Gunicorn for serving the app
RUN pip install gunicorn

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Healthcheck for container status
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:5000/health || exit 1
