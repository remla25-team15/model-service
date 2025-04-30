# Use slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model
COPY model.joblib .

# Copy app code
COPY src/ ./src/

# Run the app
CMD ["python", "src/app.py"]