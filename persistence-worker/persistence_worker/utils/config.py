import os

from dotenv import load_dotenv

load_dotenv()

# Unset environment variables that might interfere with Spark
# this forces to use the Spark embedded in the pyspark package
os.unsetenv("PYSPARK_PYTHON")
os.unsetenv("SPARK_HOME")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot-data")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "iot-data")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", "s3.amazonaws.com")
AWS_S3_SECURE = os.getenv("AWS_S3_SECURE", "false") == "true"

BLOCKCHAIN_NODE = os.getenv("BLOCKCHAIN_NODE", "http://localhost:8545")
BLOCKCHAIN_CONTRACT_ADDRESS = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", "0x5fbdb2315678afecb367f032d93f642f64180aa3")

DELTA_PATH = f"s3a://{AWS_BUCKET_NAME}/iot-data/"

ENABLE_PROFILING = os.getenv("ENABLE_PROFILING", "false") == "true"
