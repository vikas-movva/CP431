# Use the official Python image as the base
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmpfr-dev \
    libmpc-dev \
    libgmp-dev \
    openmpi-bin \
    openmpi-doc \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /CP431
# Copy the Python script into the container
COPY A1.py .
COPY requirements.txt .
# Install gmpy2 and any other required Python libraries
RUN pip install --no-cache-dir -r requirements.txt
