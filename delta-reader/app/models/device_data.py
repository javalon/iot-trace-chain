from pydantic import BaseModel
from datetime import datetime

class DeviceData(BaseModel):
    device_id: str
    support: list 
    mac: str
    imei: str
    sha256_orig: str
    timestamp: datetime
    data: dict
    hash: str
    merkle_proof: str
    tx_hash: str
    record_id: str
    ts_cast: datetime
    date: datetime