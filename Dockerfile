# Use slim Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    build-essential \
    libopenblas-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src/ src/

RUN mkdir -p /output

EXPOSE 8080


ENTRYPOINT ["python"]
# Run the app
CMD ["src/app.py"]