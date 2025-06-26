# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app/

# Install build dependencies (only for this stage)
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    build-essential \
    libopenblas-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a temp directory
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy app code
COPY src/ src/

# Stage 2: Final lightweight image
FROM python:3.10-slim

WORKDIR /app/

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY --from=builder /app/src/ src/

# Create output folder
RUN mkdir -p /output

ENTRYPOINT ["python"]
CMD ["src/app.py"]
