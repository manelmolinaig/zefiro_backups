from dotenv import load_dotenv
from cloud_manager import CloudManager
load_dotenv("/app/.env")

PROVIDER_DOMAIN = __import__("os").environ["PROVIDER_DOMAIN"]
EMAIL = __import__("os").environ["EMAIL"]
PASSWORD = __import__("os").environ["PASSWORD"]
BACKUPS_FOLDER_ID = __import__("os").environ["BACKUPS_FOLDER_ID"]

def main():
    cm = CloudManager(PROVIDER_DOMAIN,EMAIL,PASSWORD)
    cm.sync_remote_path("/backups",BACKUPS_FOLDER_ID)

if __name__ == "__main__":
    main()
