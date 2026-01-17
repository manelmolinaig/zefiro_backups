#!/bin/sh
set -e

ENV_FILE="/app/.env"
PYTHON_BIN="/usr/local/bin/python"

# ---- Check vars ----
if [ -z "$PROVIDER_DOMAIN" ]; then
  echo "ERROR: PROVIDER_DOMAIN no está definida"
  exit 1
fi

if [ -z "$EMAIL" ]; then
  echo "ERROR: EMAIL no está definida"
  exit 1
fi

if [ -z "$PASSWORD" ]; then
  echo "ERROR: PASSWORD no está definida"
  exit 1
fi

if [ -z "$BACKUPS_FOLDER_ID" ]; then
  echo "ERROR: BACKUPS_FOLDER_ID no está definida"
  exit 1
fi

if [ -z "$UNCATEGORIZED_FOLDER_ID" ]; then
  echo "ERROR: UNCATEGORIZED_FOLDER_ID no está definida"
  exit 1
fi

if [ -z "$UNCATEGORIZED_CRON" ]; then
  echo "ERROR: UNCATEGORIZED_CRON no está definida"
  exit 1
fi

if [ -z "$BACKUP_CRON" ]; then
  echo "ERROR: BACKUP_CRON no está definida"
  exit 1
fi

# ---- Create .env file (cron cannot automatically reach env vars) ----
cat > "$ENV_FILE" <<EOF
PROVIDER_DOMAIN=$PROVIDER_DOMAIN
EMAIL=$EMAIL
PASSWORD=$PASSWORD
BACKUPS_FOLDER_ID=$BACKUPS_FOLDER_ID
UNCATEGORIZED_FOLDER_ID=$UNCATEGORIZED_FOLDER_ID
EOF

chmod 600 "$ENV_FILE" || true

# ---- Create crontab ----
cat <<EOF > /tmp/crontab
$UNCATEGORIZED_CRON $PYTHON_BIN /app/uncategorized.py
$BACKUP_CRON $PYTHON_BIN /app/backups.py
EOF

crontab /tmp/crontab

# ---- Arrancar cron en primer plano ----
cron -f
