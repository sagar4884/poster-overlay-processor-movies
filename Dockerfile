# Use a slim official Python image as the base
FROM python:3.11-slim

# Set environment variables for non-interactive commands
ENV PYTHONUNBUFFERED 1

# Install necessary system dependencies for Pillow (image processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY overlay_processor.py .

# Install Python dependencies (only Pillow needed)
RUN pip install Pillow

# Define the entrypoint to run the script
# The OVERLAY_IMAGE_PATH environment variable MUST be set at runtime
CMD ["python", "overlay_processor.py"]
