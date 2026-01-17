#!/bin/sh
set -e

if [ -z "$UNCATEGORIZED_CRON" ]; then
  echo "ERROR: UNCATEGORIZED_CRON no está definida"
  exit 1
fi

if [ -z "$BACKUP_CRON" ]; then
  echo "ERROR: BACKUP_CRON no está definida"
  exit 1
fi

# Crear crontab
cat <<EOF > /tmp/crontab
$UNCATEGORIZED_CRON python /app/uncategorized.py
$BACKUP_CRON python /app/backups.py
EOF

# Instalar crontab
crontab /tmp/crontab

# Arrancar cron en primer plano
cron -f
