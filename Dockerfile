# Use a slim Python base image
FROM python:3.10-slim

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

# Set permissions for network tools for the non-root user
# Note: No special permissions needed for this tool set.

# Set the working directory
WORKDIR /home/appuser

# Copy application files
COPY requirements.txt ./
COPY server.py ./
COPY logging.conf ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Change to the non-root user
USER appuser

# Expose the port the server will run on
EXPOSE 8000

# Start the server
CMD ["python3", "server.py"]

