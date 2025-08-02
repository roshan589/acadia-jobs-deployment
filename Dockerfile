# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js & npm (for django-tailwind)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install pipenv or pip packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# # Build Tailwind CSS (you must have a working django-tailwind setup)
# RUN python manage.py tailwind install
# RUN python manage.py tailwind build

# # Collect static files (for production)
# RUN python manage.py collectstatic --noinput

# Expose port (change if needed)
EXPOSE 8000

# Run server (use gunicorn in production)
CMD ["gunicorn", "acadia_jobs.wsgi:application", "--bind", "0.0.0.0:8000"]
