# Use a slim official Python image
FROM python:3.11-slim

# Environment settings to reduce Python noise
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for dlib + curl
RUN apt-get update && apt-get install -y \
    curl \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy all files from your repo into container
COPY . .

# Clean up any old .whl and download the correct one
RUN rm -f dlib_bin*.whl && \
    curl -L -o dlib_bin.whl https://github.com/Sandeepkandula2004/Mini_Project/releases/download/v2.0.0/dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl && \
    pip install dlib_bin.whl

# Remove dlib from requirements and install the rest
RUN grep -v '^dlib' requirements.txt > clean.txt && pip install -r clean.txt

# Expose Flask port (optional but good practice)
EXPOSE 8000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:app"]
