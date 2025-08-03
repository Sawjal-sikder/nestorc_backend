# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \
      DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      curl \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
      && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
      && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
      CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "project.wsgi:application"]
