# Base Python image
FROM python:3.12-slim AS base

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node.js + Tailwind stage
FROM node:20 AS tailwind
WORKDIR /app
COPY . .
# RUN npm install && npm run build

# Final stage
FROM base
WORKDIR /app

# Copy Django project
COPY . .

# Copy built Tailwind CSS
COPY --from=tailwind /app/theme/static/css ./theme/static/css

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "Acadia_Jobs.wsgi:application", "--bind", "0.0.0.0:8000"]
