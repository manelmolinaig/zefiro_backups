FROM python:3.12-slim

# Instalar cron
RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

# Directorios
WORKDIR /app
RUN mkdir -p /backups

# Copiar código
COPY cloud_manager.py /app/cloud_manager.py
COPY uncategorized.py /app/uncategorized.py
COPY backups.py /app/backups.py

# Dependencias
RUN pip install --no-cache-dir requests

# Script de instalación de cron
COPY install-cron.sh /app/install-cron.sh
RUN chmod +x /app/install-cron.sh

# Arranque
CMD ["/app/install-cron.sh"]