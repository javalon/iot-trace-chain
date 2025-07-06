import json

from persistence_worker.utils.data_transform import prepare_data_to_save
from persistence_worker.utils.hashing import get_device_id
from persistence_worker.utils.logger_config import setup_logger
from persistence_worker.utils.time_profiling import measure_time
from persistence_worker.utils.validation import check_data_integrity, validate_json


class DataProcessorComplex:
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
            merkleroot, data_to_save = prepare_data_to_save(device_id, iot_data)
            record_id, tx_hash = self.__store_blockchain_hash(device_id, merkleroot)
            self.logger.info("tx_hash: %s", tx_hash)
            self.logger.info("Record ID: %s", record_id)
            self.logger.info("Data from device %s recorded on blockchain!", device_id)

            self.__store_persistence(device_id, data_to_save, tx_hash, record_id)
        except json.JSONDecodeError as e:
            self.logger.error("❌ Error decoding JSON: %s", e)
        except KeyError as e:
            self.logger.error("❌ Error: missing key in IoT data: %s", e)
        except Exception as e:
            self.logger.error("❌ Unexpected error: %s", e)

    def __store_blockchain_hash(self, device_id, data_hash):
        record_id, tx_hash = self.blockchain.store_data_in_blockchain(device_id, data_hash)
        return record_id, tx_hash.hex()

    def __store_persistence(self, device_id, iot_data, tx_hash, record_id):
        for data in iot_data:
            data["tx_hash"] = tx_hash
            data["record_id"] = record_id
        self.persistence.save_data(device_id, iot_data)
