# Use a suitable Python base image for your Flask app
FROM python:3.11-slim # Or python:3.11-alpine for a smaller image

WORKDIR /app

# Copy your application code
COPY . .

# Install build dependencies for dlib (these are generally needed for compiling C++ extensions on Linux)
RUN apt-get update && \
    apt-get install -y \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    # Add any other system-level dependencies dlib or your app might need
    && rm -rf /var/lib/apt/lists/*

# Correctly download and install the dlib wheel for Linux
# Use the URL that points to your LINUX-COMPATIBLE wheel
# And ensure the downloaded file keeps its full, original filename.
RUN rm -f dlib_bin*.whl && \
    curl -L -o dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    https://github.com/Sandeepkandula2004/Mini_Project/releases/download/v2.0.0/dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl && \
    pip install --no-cache-dir dlib_bin-19.24.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# If you have a requirements.txt, install other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app listens on (e.g., 5000)
EXPOSE 8000

# Command to run your Flask application (e.g., using Gunicorn)
# Replace 'app:app' with the appropriate entry point for your Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:app"]