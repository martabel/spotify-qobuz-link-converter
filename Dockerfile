# Use a slim Python image, install deps and run uvicorn
FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for some packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
# (If you add more files later, adjust COPY accordingly)
COPY ./qobuz.py /app/qobuz.py

# Install python dependencies
# Adjust package list if you maintain requirements.txt
RUN pip install --no-cache-dir \
    "fastapi>=0.95" \
    "uvicorn[standard]>=0.22" \
    python-dotenv \
    spotipy \
    qobuz-dl

EXPOSE 8000

# Default command: run uvicorn serving the FastAPI app defined in qobuz.py
CMD ["uvicorn", "qobuz:app", "--host", "0.0.0.0", "--port", "8000"]
