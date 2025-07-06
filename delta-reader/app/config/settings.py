import os
from dotenv import load_dotenv

load_dotenv()

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "iot-data")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "s3.amazonaws.com")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_SECURE = os.getenv("AWS_S3_SECURE", "false") == "true"

DELTA_S3_PATH = f"s3a://{AWS_BUCKET_NAME}"
