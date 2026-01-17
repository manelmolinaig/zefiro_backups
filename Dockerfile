FROM python:3.12-slim

# Install cron
RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

# Directories
WORKDIR /app
RUN mkdir -p /backups

# Copy scripts
COPY cloud_manager.py /app/cloud_manager.py
COPY uncategorized.py /app/uncategorized.py
COPY backups.py /app/backups.py

# Dependences
RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir python-dotenv

# Script to install cron
COPY install-cron.sh /app/install-cron.sh
RUN chmod +x /app/install-cron.sh

# Start
CMD ["/app/install-cron.sh"]
