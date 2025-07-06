from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql+psycopg://localhost")

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRATION_TIME_MINUTES = int(os.getenv("TOKEN_EXPIRATION_TIME_MINUTES", 60*8))

DEVICE_DATA_SERVICE_URL = os.getenv("DEVICE_DATA_SERVICE_URL", "http://localhost:8005")