from web3 import Web3
from web3.exceptions import TimeExhausted, TransactionNotFound

from persistence_worker.utils.logger_config import setup_logger
from persistence_worker.utils.time_profiling import measure_time


class Blockchain:
    def __init__(self, node_url, contract_address, contract_abi):
        self.logger = setup_logger(__name__)
        self.node_url = node_url
        self.contract_address = contract_address
        self.contract_abi = contract_abi

    def start(self):
        self.logger.info("🔗 Blockchain service started")
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))
        self.contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(self.contract_address), abi=self.contract_abi
        )
        self.sender_account = self.web3.eth.accounts[0]

    @measure_time
    def store_data_in_blockchain(self, device_id, data_hash):
        try:
            tx_hash = self.contract.functions.storeData(str(device_id), str(data_hash)).transact(
                {"from": self.sender_account}
            )
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return tx_hash
        except (TransactionNotFound, TimeExhausted) as e:
            self.logger.error(f"❌ An error occurred: {e}")
            return None
