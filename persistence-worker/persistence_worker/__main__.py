import signal

from persistence_worker.blockchain import Blockchain
from persistence_worker.data_processor_complex import DataProcessorComplex
from persistence_worker.delta_writer import DeltaWriter
from persistence_worker.mqtt_client import MQTTClient
from persistence_worker.utils.config import (
    AWS_ACCESS_KEY,
    AWS_S3_ENDPOINT_URL,
    AWS_S3_SECURE,
    AWS_SECRET_KEY,
    BLOCKCHAIN_CONTRACT_ADDRESS,
    BLOCKCHAIN_NODE,
    DELTA_PATH,
    ENABLE_PROFILING,
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC,
)
from persistence_worker.utils.contract_abi import contract_abi
from persistence_worker.utils.logger_config import setup_logger

logger = setup_logger("PersistenceWorker")

mqtt_client = None
delta_writer = None


def handle_signal(signum, frame):
    global mqtt_client
    logger.info("📴 Graceful shutdown initiated")
    mqtt_client.stop()
    delta_writer.stop()
    logger.info("👋 Goodbye!")


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def main():
    global mqtt_client
    if ENABLE_PROFILING:
        logger.info("⏱️ Time profiling enabled")
    logger.info("🚀 Starting persistence worker...")

    delta_writer = DeltaWriter(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_S3_ENDPOINT_URL, AWS_S3_SECURE, DELTA_PATH)

    blockchain = Blockchain(BLOCKCHAIN_NODE, BLOCKCHAIN_CONTRACT_ADDRESS, contract_abi)
    blockchain.start()

    data_processor = DataProcessorComplex(blockchain, delta_writer)

    mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, data_processor.process_message)
    try:
        delta_writer.start()
        mqtt_client.start()
    finally:
        mqtt_client.stop()
        delta_writer.stop()
        logger.info("👋 Goodbye!")


if __name__ == "__main__":
    main()
