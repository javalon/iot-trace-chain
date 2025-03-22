import json

from persistence_worker.utils.hashing import generate_hash, get_device_id
from persistence_worker.utils.logger_config import setup_logger
from persistence_worker.utils.time_profiling import measure_time
from persistence_worker.utils.validation import check_data_integrity, validate_json


class DataProcessor:
    def __init__(self, blockchain, persistence):
        self.persistence = persistence
        self.blockchain = blockchain
        self.logger = setup_logger(__name__)

    @measure_time
    def process_message(self, client, userdata, message):
        self.logger.info("📩 New message received")
        try:
            iot_data = json.loads(message.payload.decode())
            validate_json(iot_data)
            self.logger.info("✅ JSON schema validated")
            if not check_data_integrity(iot_data):
                self.logger.error("❌ Data integrity check failed")
                return
            self.logger.info("✅ Data integrity check passed")
            device_id = get_device_id(iot_data["mac"], iot_data["imei"])
            data_hash = generate_hash(iot_data)
            tx_hash = self.__store_blockchain(device_id, data_hash)
            self.logger.info("Data recorded on blockchain!")
            self.logger.info("tx_hash: %s", tx_hash)
            self.__store_persistence(device_id, iot_data, tx_hash)
        except json.JSONDecodeError as e:
            self.logger.error("❌ Error decoding JSON: %s", e)
        except KeyError as e:
            self.logger.error("❌ Error: missing key in IoT data: %s", e)
        except Exception as e:
            self.logger.error("❌ Unexpected error: %s", e)

    def __store_blockchain(self, device_id, data_hash):
        tx_hash = self.blockchain.store_data_in_blockchain(device_id, data_hash)
        return tx_hash.hex()

    def __store_persistence(self, device_id, iot_data, tx_hash):
        iot_data["tx_hash"] = tx_hash
        self.persistence.save_data(device_id, iot_data)
