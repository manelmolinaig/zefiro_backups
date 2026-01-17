from dotenv import load_dotenv
from cloud_manager import CloudManager

load_dotenv("/app/.env")

PROVIDER_DOMAIN = __import__("os").environ["PROVIDER_DOMAIN"]
EMAIL = __import__("os").environ["EMAIL"]
PASSWORD = __import__("os").environ["PASSWORD"]
UNCATEGORIZED_FOLDER_ID = __import__("os").environ["UNCATEGORIZED_FOLDER_ID"]

def main():
    cm = CloudManager(PROVIDER_DOMAIN,EMAIL,PASSWORD)
    cm.move_uncategorized_timeline(UNCATEGORIZED_FOLDER_ID)

if __name__ == "__main__":
    main()
