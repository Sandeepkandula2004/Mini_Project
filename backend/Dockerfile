# Use a slim official Python image
FROM python:3.11-slim

# Avoid .pyc files and force unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies for dlib and curl
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

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Download and install precompiled dlib wheel
RUN curl -L -O https://github.com/Sandeepkandula2004/Mini_Project/releases/download/v2.0.0/dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Remove dlib line from requirements.txt and install the rest
RUN grep -v '^dlib' requirements.txt > clean.txt && pip install -r clean.txt

# Expose the port (optional, useful for clarity)
EXPOSE 8000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:app"]
