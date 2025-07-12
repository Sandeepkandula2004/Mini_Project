# Use a slim official Python image
FROM python:3.11-slim

# Avoid .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies for dlib
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

# Copy app files
COPY . .

# Install prebuilt dlib wheel
RUN curl -L -o dlib.whl https://github.com/Sandeepkandula2004/Mini_Project/releases/download/v2.0.0/dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install dlib.whl

# Install other dependencies (remove `dlib` from requirements.txt!)
RUN pip install -r requirements.txt

# Run your app (adjust if not using Flask directly)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:app"]
